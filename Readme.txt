
# Climaview - Climate Data Visualization Web Application

## Overview
Climaview is a web-based application that visualizes climate data using real-time integration from OpenWeather API and historical data using Meteostat API. It provides users with interactive charts, maps, and administrative tools to explore global and regional climate patterns.

## Features
1. **Interactive Maps**: View climate metrics like CO₂ levels, temperatures, and weather conditions globally.
2. **Real-Time Data Integration**: Fetch live climate data using OpenWeather API.
3. **Historical Data Visualization**: Use Meteostat API to display historical climate trends (temperature and wind data).
4. **Authentication**: Login and registration features with role-based access control (admin and user).
5. **Admin Panel**: Manage users and content via the admin dashboard.

---

## Installation Instructions

Follow these steps to set up the application:

### 1. Install Dependencies
Ensure Python 3.x is installed on your system. Then, install the required Python packages using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### 2. Configure the Database
1. Install MySQL and create a database named `climaview`.
2. Open MySQL and execute the following SQL commands to create the required tables:
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user'
);

CREATE TABLE climate_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(255),
    temperature FLOAT,
    co2 FLOAT,
    humidity INT,
    pressure INT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```
3. Update the database credentials in `app.py` under the section:
```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'yourpassword'
app.config['MYSQL_DB'] = 'climaview'
```
Replace `yourpassword` with your MySQL root password.

### 3. API Keys

#### OpenWeather API Key
You can use the existing API key below if you don't want to generate a new one:
```python
API_KEY = "603fc3bac5b0d505c32e553230cdd0db"  # Existing API Key used in the code
```
If you prefer to use your own key:
- Register at [OpenWeather](https://openweathermap.org/) and copy your API key.
- Replace the placeholder API key in `app.py`.

#### Meteostat API Key
For historical weather data, the application uses the **Meteostat API**. You can use the existing API key or register for a new one:
```python
METEOSTAT_API_KEY = "0b9cd91aebmshca93482a318a47bp1fcb9fjsn93c9228ae834"  # Existing API Key used in the code
METEOSTAT_API_HOST = "meteostat.p.rapidapi.com"
```
To generate your own key:
- Sign up at [RapidAPI - Meteostat](https://rapidapi.com/meteostat/api/meteostat).
- Replace the API key and host in `app.py`:
```python
headers = {
    "x-rapidapi-key": "your_meteostat_api_key",
    "x-rapidapi-host": "meteostat.p.rapidapi.com"
}
```

---

## File Structure
```
climaview/
|-- data/
|   |-- GlobalLandTemperaturesByCity.csv  # Sample climate data
|
|-- static/
|   |-- css/
|   |-- favicon_io/
|   |-- images/
|   |-- js/
|   |-- random/
|   |-- earth-background.jpg  # Background image for visuals
|   |-- styles.css            # Main CSS file
|
|-- templates/
|   |-- about.html
|   |-- admin.html
|   |-- chart.html
|   |-- green_technologies_2024.html
|   |-- index.html
|   |-- login.html
|   |-- map.html
|   |-- register.html
|   |-- sustainability.html
|   |-- understanding_climate_change.html
|
|-- app.py                # Main Flask application file
|-- requirements.txt      # Python dependencies
|-- README.txt            # Documentation
```

---

## Run the Application
1. Start the Flask application:
```bash
flask run
```
2. Access the application at:
```
http://127.0.0.1:5000/
```

---

## Admin Login Credentials
To access the admin panel, use the following default credentials:
- **Email**: `admin@example.com`
- **Password**: `adminpassword`

You can create an admin user by inserting it into the database:
```sql
INSERT INTO users (username, email, password, role)
VALUES ('admin', 'admin@example.com', '<hashed_password>', 'admin');
```
Use [bcrypt](https://bcrypt-generator.com/) to generate the hashed password.

---

## Additional Notes
1. Ensure all dependencies are installed before running the application.
2. Verify MySQL service is running and accessible.
3. API limits for OpenWeather and Meteostat may apply.

For any issues, refer to the application log in your terminal for debugging.

---

This setup ensures your professor can easily run and evaluate the application.
