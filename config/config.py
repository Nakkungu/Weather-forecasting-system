import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Central configuration class"""
    
    # API Keys
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
    
    # Database settings
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'weather_forecast.db')
    
    # Data collection settings
    CITIES = os.getenv('CITIES', 'New York,London,Tokyo,Paris,Sydney').split(',')
    COLLECTION_INTERVAL_HOURS = int(os.getenv('COLLECTION_INTERVAL_HOURS', '1'))
    HISTORICAL_DAYS = int(os.getenv('HISTORICAL_DAYS', '30'))
    
    # Rate limiting
    API_DELAY_SECONDS = float(os.getenv('API_DELAY_SECONDS', '1.0'))
    
    # Data export
    EXPORT_DIR = os.getenv('EXPORT_DIR', 'data')
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.OPENWEATHER_API_KEY:
            raise ValueError("OPENWEATHER_API_KEY environment variable is required")
        
        if not os.path.exists(cls.EXPORT_DIR):
            os.makedirs(cls.EXPORT_DIR, exist_ok=True)
    
    @classmethod
    def display(cls):
        """Display current configuration (without sensitive data)"""
        print("=== Weather Pipeline Configuration ===")
        print(f"Cities: {', '.join(cls.CITIES)}")
        print(f"Collection interval: {cls.COLLECTION_INTERVAL_HOURS} hours")
        print(f"Database path: {cls.DATABASE_PATH}")
        print(f"Export directory: {cls.EXPORT_DIR}")
        print(f"API delay: {cls.API_DELAY_SECONDS} seconds")
        print(f"API key configured: {'Yes' if cls.OPENWEATHER_API_KEY else 'No'}")