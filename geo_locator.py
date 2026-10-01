import logging
import requests

log = logging.getLogger(__name__)

def get_location(api_url, fallback_city):
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        city = data.get('city')
        loc = data.get('loc')

        if city and loc:
            lat, lon = loc.split(',')
            return city, lat, lon

    except Exception as e:
        log.warning("GEO_API недоступен")
        return fallback_city, 55.7558, 37.6176