import asyncio
from clients.open_meteo import OpenMeteoClient
from clients.aqicn import AQICNClient

# 数据聚合器：执行并行 I/O 调度 (fetch_all_data)

async def fetch_all_data(city_name: str):
    """
    Orchestrates the data fetching process.
    1. Geocode city (Sequential, as others need lat/lon).
    2. Fetch Weather and AQI (Parallel).
    Returns tuple: (geo_data, weather_data, aqi_data)
    """
    open_meteo = OpenMeteoClient()
    aqicn = AQICNClient()

    # 1. Geocode
    geo_data = await open_meteo.search_city(city_name)
    lat = geo_data["latitude"]
    lon = geo_data["longitude"]

    # 2. Parallel Fetch
    # Use asyncio.gather for compatibility with Python < 3.11
    weather_data, aqi_data = await asyncio.gather(
        open_meteo.get_weather(lat, lon),
        aqicn.get_air_quality(lat, lon)
    )

    return geo_data, weather_data, aqi_data
