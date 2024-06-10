from dotenv import load_dotenv
import os
import requests
import mysql.connector
from datetime import datetime, timezone

# Load environment variables from .env file
load_dotenv()

def fetch_weather_data(api_key, city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    return response.json()

def store_weather_data(data):
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    cursor = conn.cursor()
    timestamp = datetime.now(timezone.utc).isoformat()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp VARCHAR(255),
            city VARCHAR(255),
            temperature FLOAT,
            feels_like FLOAT,
            pressure INT,
            humidity INT,
            weather_description VARCHAR(255)
        )
    """)
    cursor.execute("""
        INSERT INTO weather (timestamp, city, temperature, feels_like, pressure, humidity, weather_description)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        timestamp,
        data['name'],
        data['main']['temp'],
        data['main']['feels_like'],
        data['main']['pressure'],
        data['main']['humidity'],
        data['weather'][0]['description']
    ))
    conn.commit()
    cursor.close()
    conn.close()

def handler(request):
    api_key = os.getenv('API_KEY')
    city = 'Cairo'
    weather_data = fetch_weather_data(api_key, city)
    store_weather_data(weather_data)
    return {
        "statusCode": 200,
        "body": "Weather data stored successfully."
    }

if __name__ == "__main__":
    handler(None)
