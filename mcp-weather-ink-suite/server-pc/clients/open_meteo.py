import httpx
from config import Config

from services.normalizer import CityNameNormalizer

# 封装 Open-Meteo 的异步请求逻辑

class OpenMeteoClient:
    GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
    FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

    async def search_city(self, name: str):
        """
        Search for a city by name. Returns (lat, lon, country_code, city_name).
        """
        async def _execute_search(query_name):
            params = {"name": query_name, "count": 1, "format": "json"}
            # httpx automatically reads HTTPS_PROXY and HTTP_PROXY from environment
            async with httpx.AsyncClient() as client:
                resp = await client.get(self.GEOCODING_URL, params=params, timeout=10.0)
                resp.raise_for_status()
                return resp.json().get("results", [])

        # 1. First Attempt
        results = await _execute_search(name)
        
        # 2. Fallback: Normalize City Name (e.g. "大理" -> "Dali")
        if not results:
            normalized = await CityNameNormalizer.normalize(name)
            if normalized and normalized != name:
                # print(f"DEBUG: Normalized '{name}' -> '{normalized}'") # Optional logging
                results = await _execute_search(normalized)

        if not results:
            raise ValueError(f"City not found: {name}")
        
        result = results[0]
        country_name = result.get('country', 'Unknown')
        # Use strict mapping from Config
        country_code = Config.COUNTRY_CODES.get(country_name)
        if not country_code:
            # Fallback logic: first 3 chars upper
             country_code = country_name[:3].upper() if len(country_name) >= 3 else country_name.upper()

        return {
            "latitude": result.get("latitude"),
            "longitude": result.get("longitude"),
            "country_code": country_code,
            "city_name": result.get("name"),
            "timezone": result.get("timezone") # Some geocoding results include timezone
        }

    async def get_weather(self, lat: float, lon: float):
        """
        Get current weather conditions.
        """
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,weather_code,wind_speed_10m",
            "timezone": "auto"
        }
        # httpx automatically reads HTTPS_PROXY and HTTP_PROXY from environment
        async with httpx.AsyncClient() as client:
            resp = await client.get(self.FORECAST_URL, params=params, timeout=10.0)
            resp.raise_for_status()
            data = resp.json()
            current = data.get("current", {})
            return {
                "temperature": current.get("temperature_2m"),
                "weather_code": current.get("weather_code"),
                "wind_speed": current.get("wind_speed_10m"),
                "timezone": data.get("timezone"),
                "utc_offset_seconds": data.get("utc_offset_seconds", 0)
            }
