import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import requests
from flask import Flask, render_template, abort
from jinja2 import TemplateNotFound
from datetime import datetime, timedelta
import plotly
import plotly.graph_objects as go
import json
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Database Configuration
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT'))
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")

mysql = MySQL(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


# User Loader
@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if user:
        class User:
            is_authenticated = True
            is_active = True
            is_anonymous = False

            def __init__(self, id, username, email, role):
                self.id = id
                self.username = username
                self.email = email
                self.role = role

            def get_id(self):
                return str(self.id)

        return User(user[0], user[1], user[2], user[4])  # Ensure email and role are passed
    return None


# OpenWeatherMap API key
API_KEY = os.getenv("OPENWEATHER_API_KEY")


# Function to fetch CO2 data from OpenWeatherMap API
def get_co2_data(lat, lon):
    url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        co2 = data['list'][0]['components']['co']
        return co2
    return None


# Function to fetch temperature, weather patterns (description, humidity, pressure), and sea level data
def get_weather_data(lat, lon):
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'  # units=metric for Celsius
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        temperature = data['main']['temp']
        sea_level = data['main'].get('sea_level', 'N/A')  # Sea level is optional, may not be available in all responses
        weather_description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        return {
            'temperature': temperature,
            'sea_level': sea_level,
            'weather_description': weather_description,
            'humidity': humidity,
            'pressure': pressure
        }
    return None


# Route to handle getting weather data (CO2, temperature, sea level, weather patterns)
@app.route('/get_weather_data')
def weather_data():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)

    # Fetch CO2 and weather data for the given coordinates
    co2 = get_co2_data(lat, lon)
    weather = get_weather_data(lat, lon)

    # Return the data as JSON
    if co2 is not None and weather is not None:
        return jsonify({
            'co2': co2,
            'temperature': weather['temperature'],
            'sea_level': weather['sea_level'],
            'weather_description': weather['weather_description'],
            'humidity': weather['humidity'],
            'pressure': weather['pressure']
        })
    else:
        return jsonify({'error': 'Unable to fetch data'}), 500


# Route for the home page (map is on the main page)
@app.route('/')
def home():
    return render_template('index.html', logged_in=current_user.is_authenticated)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            # Check if password matches
            if bcrypt.check_password_hash(user[3], password):
                # Log the user in
                user_obj = load_user(user[0])
                login_user(user_obj)

                # Check for admin role and redirect
                if user[4].strip() == 'admin':  # Strip spaces and check role
                    return redirect(url_for('admin_panel'))

                # If not an admin, redirect to home
                flash("Logged in successfully!", "success")
                return redirect(url_for('home'))
            else:
                flash("Invalid credentials, try again!", "danger")
        else:
            flash("Invalid credentials, try again!", "danger")

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                           (username, email, password))
            mysql.connection.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for('login'))
        except:
            flash("User already exists.", "danger")
    return render_template('register.html')


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_panel():
    if not current_user.is_authenticated or current_user.role != 'admin':
        flash("Access denied!", "danger")
        return redirect(url_for('home'))

    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        # Handle Add, Update, or Delete based on request form data
        action = request.form.get('action')
        if action == 'add':
            username = request.form['username']
            email = request.form['email']
            password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
            cursor.execute("INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, 'user')",
                           (username, email, password))
            mysql.connection.commit()
            flash("User added successfully!", "success")
        elif action == 'update':
            user_id = request.form['user_id']
            username = request.form['username']
            email = request.form['email']
            cursor.execute("UPDATE users SET username = %s, email = %s WHERE id = %s",
                           (username, email, user_id))
            mysql.connection.commit()
            flash("User updated successfully!", "success")
        elif action == 'delete':
            user_id = request.form['user_id']
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            mysql.connection.commit()
            flash("User deleted successfully!", "success")

    cursor.execute("SELECT id, username, email, role FROM users")
    users = cursor.fetchall()
    return render_template('admin.html', users=users)


# Meteostat API details for chart
METEOSTAT_API_URL = "https://meteostat.p.rapidapi.com/stations/monthly"
METEOSTAT_API_KEY = os.getenv("METEOSTAT_API_KEY")
METEOSTAT_API_HOST = "meteostat.p.rapidapi.com"

# Default cities and their station IDs
CITIES = {
    "New York": "72503",
    "Los Angeles": "72295",
    "Chicago": "72534",
    "Houston": "72243",
    "Phoenix": "72278",
    "Philadelphia": "72408",
    "San Antonio": "72253",
    "San Diego": "72290",
    "Dallas": "72259",
    "San Jose": "72494",
    "New Jersey": "72572"
}


def fetch_weather_data(station_id, start_date, end_date):
    """Fetch monthly weather data from the Meteostat API."""
    querystring = {
        "station": station_id,
        "start": start_date,
        "end": end_date
    }
    headers = {
        "x-rapidapi-key": METEOSTAT_API_KEY,  # Updated key name
        "x-rapidapi-host": METEOSTAT_API_HOST
    }

    try:
        response = requests.get(METEOSTAT_API_URL, headers=headers, params=querystring, timeout=10)
        response.raise_for_status()
        return response.json()  # Return the parsed JSON response
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return {"error": str(http_err)}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}


@app.route('/chart')
@login_required
def chart():
    """Serve the chart page."""
    return render_template('chart.html', cities=CITIES)


@app.route('/api/data', methods=['GET'])
def get_data():
    """API endpoint to fetch weather data."""
    data_type = request.args.get('type', default='temperature', type=str)  # 'temperature' or 'wind'
    city = request.args.get('city', default='New York', type=str)
    station_id = CITIES.get(city, "72503")  # Default to New York's station

    end_date = datetime.now()
    start_date = end_date - timedelta(days=10 * 365)  # Approximate 10 years

    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    data = fetch_weather_data(station_id, start_date_str, end_date_str)
    if "error" in data:
        return jsonify(data)

    # Filter data based on the selected type
    if data_type == 'wind':
        result = [{"date": item["date"], "value": item.get("wspd", None)} for item in data.get("data", [])]
    else:  # temperature
        result = [{"date": item["date"], "value": item.get("tavg", None)} for item in data.get("data", [])]

    return jsonify({"data": result})


@app.route('/logout')
def logout():
    logout_user()
    flash("Logged out successfully!", "success")
    return redirect(url_for('home'))


@app.route('/protected')
@login_required
def protected():
    return "This is a protected route!"


# Route for the about page
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/map')
@login_required
def map():
    return render_template('map.html')


@app.route('/blog/<slug>')
@login_required
def blog(slug):
    try:
        return render_template(f'{slug}.html')
    except TemplateNotFound:
        return "Blog not found", 404

@app.route('/dashboard_data')
@login_required
def dashboard_data():
    # New York City coordinates
    lat = 40.7128
    lon = -74.0060

    co2 = get_co2_data(lat, lon)
    weather = get_weather_data(lat, lon)

    if weather:
        return jsonify({
            'temperature': weather['temperature'],
            'humidity': weather['humidity'],
            'pressure': weather['pressure'],
            'co2': co2
        })

    return jsonify({'error': 'Unable to load dashboard data'})

@app.route('/favorites')
@login_required
def favorites():

    cursor = mysql.connection.cursor()

    cursor.execute("""
    SELECT id, city_name
    FROM favorite_cities
    WHERE user_id = %s
""", (current_user.id,))

    cities = cursor.fetchall()

    return render_template(
        'favorites.html',
        cities=cities
    )

@app.route('/save_city', methods=['POST'])
@login_required
def save_city():

    city = request.form['city']

    cursor = mysql.connection.cursor()

    cursor.execute("""
    SELECT *
    FROM favorite_cities
    WHERE user_id=%s
    AND city_name=%s
    """, (current_user.id, city))

    existing_city = cursor.fetchone()

    if existing_city:
        flash("City already exists!", "warning")
        return redirect(url_for('favorites'))

    cursor.execute("""
        INSERT INTO favorite_cities
        (user_id, city_name)
        VALUES (%s, %s)
    """, (current_user.id, city))

    mysql.connection.commit()

    flash("City saved successfully!", "success")

    return redirect(url_for('favorites'))


@app.route('/delete_city/<int:city_id>')
@login_required
def delete_city(city_id):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        DELETE FROM favorite_cities
        WHERE id = %s
        AND user_id = %s
    """, (city_id, current_user.id))

    mysql.connection.commit()

    flash("City removed.", "success")

    return redirect(url_for('favorites'))


def calculate_risk(weather):

    score = 0

    temp = weather["temperature"]
    humidity = weather["humidity"]
    pressure = weather["pressure"]

    # Temperature

    if temp >= 35:
        score += 40

    elif temp >= 30:
        score += 30

    elif temp >= 25:
        score += 20

    # Humidity

    if humidity >= 85:
        score += 30

    elif humidity >= 70:
        score += 20

    elif humidity >= 60:
        score += 10

    # Pressure

    if pressure < 1000:
        score += 20

    elif pressure < 1010:
        score += 10

    # Status

    if score >= 70:
        status = "High Risk"

    elif score >= 40:
        status = "Moderate Risk"

    else:
        status = "Low Risk"

    return {
        "score": score,
        "status": status
    }

def generate_climate_insight(weather):

    city = weather["city"]

    temp = weather["temperature"]
    humidity = weather["humidity"]
    pressure = weather["pressure"]

    insight = []

    if temp >= 30:
        insight.append(
            "High temperature conditions detected."
        )

    elif temp <= 5:
        insight.append(
            "Low temperature conditions detected."
        )

    if humidity >= 80:
        insight.append(
            "Elevated humidity levels may affect comfort."
        )

    elif humidity <= 30:
        insight.append(
            "Dry atmospheric conditions observed."
        )

    if pressure < 1000:
        insight.append(
            "Low pressure may indicate unstable weather."
        )

    if len(insight) == 0:
        insight.append(
            "Current climate conditions appear stable."
        )

    return " ".join(insight)


@app.route('/compare_data')
@login_required
def compare_data():

    cities = request.args.getlist('cities')

    print("Received Cities:", cities)

    results = []

    for city in cities:

        weather = get_city_weather(city)

        if weather:

            risk = calculate_risk(weather)

            insight = generate_climate_insight(weather)

            weather["insight"] = insight

            weather["risk_score"] = risk["score"]

            weather["risk_status"] = risk["status"]

            results.append(weather)

    print("Results:", results)

    return jsonify(results)

    cities = request.args.getlist('cities')

    results = []

    for city in cities:

        weather = get_city_weather(city)

    if weather:

        risk = calculate_risk(weather)

        insight = generate_climate_insight(weather)

        weather["insight"] = insight

        weather["risk_score"] = risk["score"]

        weather["risk_status"] = risk["status"]

        results.append(weather)
    return jsonify(results)

@app.route('/dashboard')
@login_required
def dashboard():

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT id, city_name
        FROM favorite_cities
        WHERE user_id=%s
    """, (current_user.id,))

    cities = cursor.fetchall()

    return render_template(
        'dashboard.html',
        cities=cities
    )

@app.route('/dashboard_analytics')
@login_required
def dashboard_analytics():

    cities = request.args.getlist('cities')

    results = []

    for city in cities:

        weather = get_city_weather(city)

        if weather:

            risk = calculate_risk(weather)

            weather["risk_score"] = risk["score"]

            results.append(weather)

    return jsonify(results)

def get_city_weather(city):

    url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?q={city}"
        f"&appid={API_KEY}"
        f"&units=metric"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    return {
        "city": city,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"]
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port
    )