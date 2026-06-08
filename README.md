# 🌍 Climate Intelligence Dashboard

A full-stack climate analytics platform that provides real-time weather monitoring, historical climate analysis, climate risk assessment, and interactive data visualizations. The application enables users to explore climate conditions across cities worldwide while offering personalized dashboards and favorite city tracking.

---

## 🚀 Live Demo

**Application:** https://climate-intelligence-dashboard-jx6o.onrender.com

---

## 📖 Project Overview

Climate Intelligence Dashboard was developed to help users understand and monitor climate patterns through an intuitive web-based interface. The platform integrates real-time weather data, historical climate records, risk scoring algorithms, and interactive analytics to provide meaningful environmental insights.

The application allows users to compare multiple cities, track climate conditions, visualize trends, and receive climate risk assessments based on current environmental factors.

---

## ✨ Key Features

### 🔐 User Authentication

* Secure user registration and login
* Password hashing with Flask-Bcrypt
* Session management using Flask-Login
* Role-based user support

### 🌤 Real-Time Weather Monitoring

* Live weather data from OpenWeather API
* Current temperature, humidity, and atmospheric pressure
* Dynamic weather updates

### 📊 Climate Analytics Dashboard

* Multi-city climate comparison
* Interactive weather analytics
* Historical climate trend visualization
* Climate data insights

### ⚠️ Climate Risk Assessment

* Automated climate risk scoring
* Risk classification:

  * Low Risk
  * Moderate Risk
  * High Risk
* AI-style climate insight generation

### ⭐ Favorite Cities Management

* Save preferred cities
* Personalized climate watchlist
* Quick access to frequently monitored locations

### 📈 Interactive Data Visualization

* Plotly-powered charts
* Comparative climate analysis
* Historical trend visualization
* Dynamic dashboard reporting

---

## 🏗️ System Architecture

User
↓
Flask Web Application
↓
OpenWeather API + Meteostat API
↓
Climate Analytics Engine
↓
Risk Assessment Module
↓
Interactive Dashboard & Visualizations
↓
Railway MySQL Database

---

## 🛠️ Technology Stack

### Backend

* Python
* Flask
* Flask-Login
* Flask-Bcrypt
* Flask-MySQLdb

### Frontend

* HTML5
* CSS3
* JavaScript

### Database

* MySQL
* Railway Cloud Database

### APIs

* OpenWeather API
* Meteostat API

### Data Visualization

* Plotly

### Deployment

* Render
* Railway

### Version Control

* Git
* GitHub

---

## 📂 Project Structure

```text
Climate-Intelligence-Dashboard/
│
├── app.py
├── requirements.txt
├── .env
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── favicon_io/
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── admin.html
│   ├── about.html
│   └── blog pages
│
└── data/
    └── GlobalLandTemperaturesByCity.csv
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/sevandiyora/Climate-Intelligence-Dashboard.git
cd Climate-Intelligence-Dashboard
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

Windows:

```bash
.venv\Scripts\activate
```

Mac/Linux:

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
MYSQL_HOST=your_host
MYSQL_PORT=your_port
MYSQL_USER=your_user
MYSQL_PASSWORD=your_password
MYSQL_DB=your_database

OPENWEATHER_API_KEY=your_api_key
METEOSTAT_API_KEY=your_api_key

SECRET_KEY=your_secret_key
```

### Run Application

```bash
python app.py
```

---

## 📸 Application Features

### Home Page

* Climate awareness portal
* Educational climate content
* Navigation to analytics tools

### Dashboard

* Multi-city comparison
* Climate risk scoring
* Interactive analytics

### Favorites

* Personalized city watchlist
* Quick access monitoring

### Historical Analysis

* Long-term climate trends
* Comparative visualizations

---

## 🎯 Learning Outcomes

This project demonstrates practical experience with:

* Full-stack web development
* REST API integration
* User authentication systems
* Relational database design
* Cloud deployment
* Data visualization
* Environmental data analysis
* Software engineering best practices

---

## 👨‍💻 Author

**Sevan Diyora**

Master of Science in Computer Science
Montclair State University

GitHub: https://github.com/sevandiyora

LinkedIn: https://www.linkedin.com/in/sevan-diyora

---

## 📄 License

This project is intended for educational, academic, and portfolio purposes.
