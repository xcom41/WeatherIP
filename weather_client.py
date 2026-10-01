import logging
from collections import defaultdict
from datetime import datetime

import requests

log = logging.getLogger(__name__)

def weather_forecast(default_url, api_key, lat, lon):
    url = f"{default_url}/forecast"
    params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric", "lang": "ru"}
    response = requests.get(url, params=params, timeout=15)

    if response.status_code == 401:
        raise ValueError("Неверный API-ключ (401)")
    if response.status_code == 429:
        raise ValueError("Превышен лимит запросов (429)")

    response.raise_for_status()
    return response.json()

def aggregate_daily(forecast, days=4):
    days_list = defaultdict(list)
    for item in forecast["list"]:
        day = datetime.fromtimestamp(item["dt"]).date()
        days_list[day].append(item)

    result = []

    for day in sorted(days_list)[:days]:
        items = days_list[day]

        temps_min = [i["main"]["temp_min"] for i in items]
        temps_max = [i["main"]["temp_max"] for i in items]
        humidities = [i["main"]["humidity"] for i in items]
        winds = [i["wind"]["speed"] for i in items]
        descriptions = [i["weather"][0]["description"] for i in items]

        result.append({
            "date": day,
            "temp_min": min(temps_min),
            "temp_max": max(temps_max),
            "humidity": round(sum(humidities) / len(humidities)),
            "wind": max(winds),
            "description": descriptions[len(descriptions) // 2].capitalize(),
        })

    return result