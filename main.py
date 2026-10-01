import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from geo_locator import get_location
from weather_client import weather_forecast, aggregate_daily
from db_models import get_engine, init_db, save_weather, load_weather
from exporter import export

env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
WEATHER_API_BASE_URL = os.getenv("WEATHER_API_BASE_URL",
                                 "https://api.openweathermap.org/data/2.5")
GEO_API_URL = os.getenv("GEO_API_URL", "https://ipinfo.io/json")
GEO_API_FALLBACK_CITY = os.getenv("GEO_API_FALLBACK_CITY", "Moscow")
DB_URL = os.getenv("DB_URL", "sqlite:///weather_lab.db")
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "weather_report.md")

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("main")

def main():
    # Геолокация
    city, lat,lon = get_location(GEO_API_URL, GEO_API_FALLBACK_CITY)
    log.info("Локация: %s", city)

    # Погода
    temp = weather_forecast(WEATHER_API_BASE_URL, WEATHER_API_KEY, lat, lon)

    daily = aggregate_daily(temp, days=4)

    # БД
    engine = get_engine(DB_URL)
    init_db(engine)
    i = save_weather(engine, city, daily)

    # Экспорт
    rows = load_weather(engine, city)
    path = export(OUTPUT_FILE, city, rows)

    # Отчёт
    print(f"Город:        {city}")
    print(f"Координаты:   {lat}, {lon}")
    print(f"Период:       {rows[0].date} — {rows[-1].date}")
    print(f"Записей в БД: {len(rows)}")
    print(f"Файл отчёта:  {path}")
    return 0

if __name__ == "__main__":
    sys.exit(main())