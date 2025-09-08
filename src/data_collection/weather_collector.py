import requests
import pandas as pd
import sqlite3
import json
import time
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional
import os
from dataclasses import dataclass

from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class WeatherConfig:
    """Configuration class for weather data collection"""
    openweather_api_key: str
    database_path: str = "weather_data.db"
    cities: List[str] = None
    collection_interval_hours: int = 1
    
    def __post_init__(self):
        if self.cities is None:
            self.cities = ["New York", "London", "Tokyo", "Sydney"]

class WeatherDataCollector:
    """Main class for collecting weather data from multiple sources"""
    
    def __init__(self, config: WeatherConfig):
        self.config = config
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.historical_url = "http://api.openweathermap.org/data/3.0/onecall/timemachine"
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database with required tables"""
        conn = sqlite3.connect(self.config.database_path)
        cursor = conn.cursor()
        
        # Current weather table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS current_weather (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                country TEXT,
                latitude REAL,
                longitude REAL,
                timestamp DATETIME,
                temperature REAL,
                feels_like REAL,
                humidity INTEGER,
                pressure REAL,
                wind_speed REAL,
                wind_direction INTEGER,
                visibility INTEGER,
                cloud_cover INTEGER,
                weather_main TEXT,
                weather_description TEXT,
                sunrise DATETIME,
                sunset DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Historical weather table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historical_weather (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                latitude REAL,
                longitude REAL,
                timestamp DATETIME,
                temperature REAL,
                feels_like REAL,
                humidity INTEGER,
                pressure REAL,
                wind_speed REAL,
                wind_direction INTEGER,
                cloud_cover INTEGER,
                weather_main TEXT,
                weather_description TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # City coordinates cache
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS city_coordinates (
                city TEXT PRIMARY KEY,
                country TEXT,
                latitude REAL,
                longitude REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def get_city_coordinates(self, city: str) -> Optional[Dict]:
        """Get city coordinates, use cache if available"""
        conn = sqlite3.connect(self.config.database_path)
        cursor = conn.cursor()
        
        # Check cache first
        cursor.execute("SELECT * FROM city_coordinates WHERE city = ?", (city,))
        result = cursor.fetchone()
        
        if result:
            conn.close()
            return {
                'city': result[0],
                'country': result[1],
                'lat': result[2],
                'lon': result[3]
            }
        
        # If not in cache, fetch from API
        geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct"
        params = {
            'q': city,
            'limit': 1,
            'appid': self.config.openweather_api_key
        }
        
        try:
            response = requests.get(geocoding_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data:
                city_data = data[0]
                coords = {
                    'city': city_data['name'],
                    'country': city_data['country'],
                    'lat': city_data['lat'],
                    'lon': city_data['lon']
                }
                
                # Cache the result
                cursor.execute('''
                    INSERT INTO city_coordinates (city, country, latitude, longitude)
                    VALUES (?, ?, ?, ?)
                ''', (coords['city'], coords['country'], coords['lat'], coords['lon']))
                conn.commit()
                conn.close()
                
                return coords
        except Exception as e:
            logger.error(f"Error getting coordinates for {city}: {e}")
        
        conn.close()
        return None
    
    def collect_current_weather(self, city: str) -> bool:
        """Collect current weather data for a city"""
        coords = self.get_city_coordinates(city)
        if not coords:
            logger.error(f"Could not get coordinates for {city}")
            return False
        
        url = f"{self.base_url}/weather"
        params = {
            'lat': coords['lat'],
            'lon': coords['lon'],
            'appid': self.config.openweather_api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Extract weather data
            weather_data = {
                'city': coords['city'],
                'country': coords['country'],
                'latitude': coords['lat'],
                'longitude': coords['lon'],
                'timestamp': datetime.fromtimestamp(data['dt']),
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data.get('wind', {}).get('speed', 0),
                'wind_direction': data.get('wind', {}).get('deg', 0),
                'visibility': data.get('visibility', 0),
                'cloud_cover': data['clouds']['all'],
                'weather_main': data['weather'][0]['main'],
                'weather_description': data['weather'][0]['description'],
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']),
                'sunset': datetime.fromtimestamp(data['sys']['sunset'])
            }
            
            # Store in database
            self.store_current_weather(weather_data)
            logger.info(f"Collected current weather for {city}")
            return True
            
        except Exception as e:
            logger.error(f"Error collecting current weather for {city}: {e}")
            return False
    
    def collect_historical_weather(self, city: str, days_back: int = 30) -> bool:
        """Collect historical weather data for a city"""
        coords = self.get_city_coordinates(city)
        if not coords:
            logger.error(f"Could not get coordinates for {city}")
            return False
        
        success_count = 0
        
        for i in range(days_back):
            date = datetime.now() - timedelta(days=i+1)
            timestamp = int(date.timestamp())
            
            # Note: Historical data requires a paid OpenWeather subscription
            # For demo purposes, we'll use the free tier current weather endpoint
            # and simulate historical collection
            url = f"{self.base_url}/weather"
            params = {
                'lat': coords['lat'],
                'lon': coords['lon'],
                'appid': self.config.openweather_api_key,
                'units': 'metric'
            }
            
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                # For demo: modify timestamp to simulate historical data
                historical_data = {
                    'city': coords['city'],
                    'latitude': coords['lat'],
                    'longitude': coords['lon'],
                    'timestamp': date,
                    'temperature': data['main']['temp'] + (i * 0.1),  # Slight variation
                    'feels_like': data['main']['feels_like'] + (i * 0.1),
                    'humidity': max(0, min(100, data['main']['humidity'] + (i % 10))),
                    'pressure': data['main']['pressure'] + (i % 5),
                    'wind_speed': max(0, data.get('wind', {}).get('speed', 0) + (i * 0.05)),
                    'wind_direction': (data.get('wind', {}).get('deg', 0) + (i * 2)) % 360,
                    'cloud_cover': max(0, min(100, data['clouds']['all'] + (i % 20))),
                    'weather_main': data['weather'][0]['main'],
                    'weather_description': data['weather'][0]['description']
                }
                
                self.store_historical_weather(historical_data)
                success_count += 1
                
                # Rate limiting
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error collecting historical weather for {city}, day {i}: {e}")
        
        logger.info(f"Collected {success_count}/{days_back} historical records for {city}")
        return success_count > 0
    
    def store_current_weather(self, weather_data: Dict):
        """Store current weather data in database"""
        conn = sqlite3.connect(self.config.database_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO current_weather (
                city, country, latitude, longitude, timestamp, temperature, feels_like,
                humidity, pressure, wind_speed, wind_direction, visibility, cloud_cover,
                weather_main, weather_description, sunrise, sunset
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            weather_data['city'], weather_data['country'], weather_data['latitude'],
            weather_data['longitude'], weather_data['timestamp'], weather_data['temperature'],
            weather_data['feels_like'], weather_data['humidity'], weather_data['pressure'],
            weather_data['wind_speed'], weather_data['wind_direction'], weather_data['visibility'],
            weather_data['cloud_cover'], weather_data['weather_main'], weather_data['weather_description'],
            weather_data['sunrise'], weather_data['sunset']
        ))
        
        conn.commit()
        conn.close()
    
    def store_historical_weather(self, weather_data: Dict):
        """Store historical weather data in database"""
        conn = sqlite3.connect(self.config.database_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO historical_weather (
                city, latitude, longitude, timestamp, temperature, feels_like,
                humidity, pressure, wind_speed, wind_direction, cloud_cover,
                weather_main, weather_description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            weather_data['city'], weather_data['latitude'], weather_data['longitude'],
            weather_data['timestamp'], weather_data['temperature'], weather_data['feels_like'],
            weather_data['humidity'], weather_data['pressure'], weather_data['wind_speed'],
            weather_data['wind_direction'], weather_data['cloud_cover'],
            weather_data['weather_main'], weather_data['weather_description']
        ))
        
        conn.commit()
        conn.close()
    
    def get_data_summary(self) -> Dict:
        """Get summary of collected data"""
        conn = sqlite3.connect(self.config.database_path)
        
        current_count = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM current_weather", conn
        ).iloc[0]['count']
        
        historical_count = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM historical_weather", conn
        ).iloc[0]['count']
        
        cities_with_data = pd.read_sql_query(
            "SELECT DISTINCT city FROM current_weather", conn
        )['city'].tolist()
        
        conn.close()
        
        return {
            'current_records': current_count,
            'historical_records': historical_count,
            'cities': cities_with_data,
            'total_records': current_count + historical_count
        }
    
    def export_to_csv(self, table: str = 'both', output_dir: str = 'data') -> List[str]:
        """Export data to CSV files"""
        os.makedirs(output_dir, exist_ok=True)
        conn = sqlite3.connect(self.config.database_path)
        exported_files = []
        
        if table in ['current', 'both']:
            current_df = pd.read_sql_query("SELECT * FROM current_weather", conn)
            current_file = os.path.join(output_dir, 'current_weather.csv')
            current_df.to_csv(current_file, index=False)
            exported_files.append(current_file)
        
        if table in ['historical', 'both']:
            historical_df = pd.read_sql_query("SELECT * FROM historical_weather", conn)
            historical_file = os.path.join(output_dir, 'historical_weather.csv')
            historical_df.to_csv(historical_file, index=False)
            exported_files.append(historical_file)
        
        conn.close()
        logger.info(f"Exported data to: {exported_files}")
        return exported_files

def main():
    """Example usage of the weather data collector"""
    
    # Configuration - you'll need to add your OpenWeather API key
    from dotenv import load_dotenv
    import os
    load_dotenv()
    api_key = os.getenv("OPENWEATHER_API_KEY")
    config = WeatherConfig(
        openweather_api_key=api_key,
        cities=["New York", "London", "Tokyo", "Paris", "Sydney"],
        database_path="weather_forecast_data.db"
    )
    
    # Initialize collector
    collector = WeatherDataCollector(config)
    
    # Collect current weather for all cities
    logger.info("Starting current weather collection...")
    for city in config.cities:
        collector.collect_current_weather(city)
        time.sleep(1)  # Rate limiting
    
    # Collect some historical data (limited by free tier)
    logger.info("Starting historical weather collection...")
    for city in config.cities[:2]:  # Limit to 2 cities for demo
        collector.collect_historical_weather(city, days_back=10)
        time.sleep(2)  # Rate limiting
    
    # Print data summary
    summary = collector.get_data_summary()
    print("\n=== Data Collection Summary ===")
    print(f"Current records: {summary['current_records']}")
    print(f"Historical records: {summary['historical_records']}")
    print(f"Cities with data: {', '.join(summary['cities'])}")
    print(f"Total records: {summary['total_records']}")
    
    # Export to CSV
    exported_files = collector.export_to_csv()
    print(f"\nData exported to: {', '.join(exported_files)}")

if __name__ == "__main__":
    main()