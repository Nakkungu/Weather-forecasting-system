import schedule
import time
import logging
from .weather_collector import WeatherDataCollector, WeatherConfig
from config.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherScheduler:
    """Automated weather data collection scheduler"""
    
    def __init__(self):
        Config.validate()
        self.config = WeatherConfig(
            openweather_api_key=Config.OPENWEATHER_API_KEY,
            database_path=Config.DATABASE_PATH,
            cities=Config.CITIES,
            collection_interval_hours=Config.COLLECTION_INTERVAL_HOURS
        )
        self.collector = WeatherDataCollector(self.config)
    
    def collect_all_current(self):
        """Collect current weather for all configured cities"""
        logger.info("Starting scheduled current weather collection")
        success_count = 0
        
        for city in self.config.cities:
            try:
                if self.collector.collect_current_weather(city):
                    success_count += 1
                time.sleep(Config.API_DELAY_SECONDS)
            except Exception as e:
                logger.error(f"Error collecting weather for {city}: {e}")
        
        logger.info(f"Completed collection: {success_count}/{len(self.config.cities)} cities")
        
        # Export data periodically
        if success_count > 0:
            self.collector.export_to_csv()
    
    def run_continuous(self):
        """Run the scheduler continuously"""
        logger.info("Starting weather data collection scheduler")
        Config.display()
        
        # Schedule regular collection
        schedule.every(Config.COLLECTION_INTERVAL_HOURS).hours.do(self.collect_all_current)
        
        # Initial collection
        self.collect_all_current()
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def run_once(self):
        """Run collection once"""
        self.collect_all_current()
        summary = self.collector.get_data_summary()
        print(f"\nCollection complete. Total records: {summary['total_records']}")

if __name__ == "__main__":
    scheduler = WeatherScheduler()
    scheduler.run_once()  # Change to run_continuous() for automated collection