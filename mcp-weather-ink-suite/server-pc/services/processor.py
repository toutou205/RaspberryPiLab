from datetime import datetime
from utils.datetime_tool import get_local_time, format_timestamp

# result processor
# 数据处理器：清洗数据、时区转换、WMO 编码转换

WMO_CODES = {
    0: "Sunny / Clear", 
    1: "Mainly Clear", 
    2: "Partly Cloudy", 
    3: "Overcast",
    45: "Fog", 
    48: "Rime Fog",
    51: "Drizzle", 
    53: "Drizzle", 
    55: "Drizzle",
    56: "Freezing Rain", 
    57: "Freezing Rain",
    61: "Light Rain", 
    63: "Moderate Rain", 
    65: "Heavy Rain",
    66: "Freezing Rain", 
    67: "Freezing Rain",
    71: "Lt Snow/Grain", 
    73: "Moderate Snow", 
    75: "Heavy Snow",
    77: "Lt Snow/Grain",
    80: "Shower Rain", 
    81: "Shower Rain", 
    82: "Heavy Showers",
    85: "Snow Shower", 
    86: "Snow Shower",
    95: "Thunderstorm", 
    96: "T-Storm w/Hail", 
    99: "T-Storm w/Hail"
}

def decode_wmo_code(code: int) -> str:
    """Converts WMO weather code to human-readable string (English)."""
    return WMO_CODES.get(code, "Unknown")

def process_logic(geo_data: dict, weather_data: dict, aqi_data: dict) -> dict:
    """
    Combines raw data from different sources into a clean dictionary.
    Handles timezone conversion and formatting.
    """
    # 1. Decode WMO Code
    wmo_code = weather_data.get("weather_code", 0)
    weather_desc = decode_wmo_code(wmo_code)

    # 2. Timezone Handling
    timezone_str = weather_data.get("timezone", "")
    utc_offset = weather_data.get("utc_offset_seconds", 0)
    
    # If geo_data has timezone, it might be better, but weather API usually gives local time context
    # However, weather_only.py logic suggests using timezone from weather API or falling back.
    if not timezone_str and geo_data.get("timezone"):
        timezone_str = geo_data.get("timezone")

    local_dt = get_local_time(timezone_str, utc_offset)
    formatted_time = format_timestamp(local_dt)

    # 3. Assemble Data
    return {
        "country_code": geo_data.get("country_code", "UNK"),
        "city_name": geo_data.get("city_name", "Unknown"),
        "timestamp": formatted_time,
        "weather_code": wmo_code,
        "weather_desc": weather_desc,
        "temperature": weather_data.get("temperature", 0.0),
        "aqi": aqi_data.get("aqi", 0),
        "pm25": aqi_data.get("pm25", 0.0)
    }
