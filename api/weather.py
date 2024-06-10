import os
import requests
import sqlite3
from datetime import datetime, timezone

def fetch_weather_data(api_key, city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    return response.json()

def store_weather_data(data):
    conn = sqlite3.connect('/tmp/weather_data.db')
    timestamp = datetime.now(timezone.utc).isoformat()
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS weather (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                city TEXT,
                temperature REAL,
                feels_like REAL,
                pressure INTEGER,
                humidity INTEGER,
                weather_description TEXT
            )
        """)
        conn.execute("""
            INSERT INTO weather (timestamp, city, temperature, feels_like, pressure, humidity, weather_description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            timestamp,
            data['name'],
            data['main']['temp'],
            data['main']['feels_like'],
            data['main']['pressure'],
            data['main']['humidity'],
            data['weather'][0]['description']
        ))

def handler(request):
    api_key = os.getenv('3d0b24e208b16d7a860fffce574a888e')
    city = 'Cairo'
    weather_data = fetch_weather_data(api_key, city)
    store_weather_data(weather_data)
    return {
        "statusCode": 200,
        "body": "Weather data stored successfully."
    }
