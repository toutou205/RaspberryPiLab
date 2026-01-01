# Usage Example: Integrating with Other MCP Servers

This document shows how to use the `pi-sense-display` MCP server together with `open-meteo` and `aqicn-air-quality` servers to display weather information.

## Workflow Overview

1. **City Name Translation**: Convert Chinese city name to English (if needed)
2. **Get Coordinates**: Use `open-meteo.search_city()` to get latitude/longitude
3. **Get Weather Data**: Use `open-meteo.get_weather_forecast()` to get current weather
4. **Get Air Quality**: Use `aqicn-air-quality.city_aqi()` to get AQI data
5. **Format Timestamp**: Generate formatted timestamp string
6. **Generate Warning Message**: Use LLM to generate health advice
7. **Display**: Call `pi-sense-display.display_weather_info()` with formatted data

## Example: Display Weather for 青岛 (Qingdao)

### Step 1: Search for City Coordinates

```python
# Call open-meteo MCP server
result = await mcp_client.call_tool("open-meteo", "search_city", {"name": "Qingdao"})
# Returns: "Location Found: Qingdao (China)\nLatitude: 36.0671\nLongitude: 120.3826"

# Parse coordinates
lat = 36.0671
lon = 120.3826
```

### Step 2: Get Weather Data

```python
# Call open-meteo MCP server
weather_result = await mcp_client.call_tool(
    "open-meteo", 
    "get_weather_forecast", 
    {"latitude": lat, "longitude": lon}
)

# Parse result (example format):
# "--- Weather Report ---
# Condition: Moderate Rain (中雨)
# Temperature: 7.0°C
# Feels Like: 5.0°C
# Humidity: 48%
# Wind: 1.5 km/h (Dir: 190°)
# ----------------------"

# Extract: weather_code = 63, weather_desc = "Moderate Rain", temperature = 7.0
```

### Step 3: Get Air Quality Data

```python
# Call aqicn-air-quality MCP server
aqi_result = await mcp_client.call_tool(
    "aqicn-air-quality",
    "city_aqi",
    {"city": "Qingdao"}
)

# Parse JSON result:
# {
#   "aqi": 152,
#   "dominentpol": "pm25",
#   "iaqi": {
#     "pm25": {"v": 152},
#     "pm10": {"v": 63},
#     "t": {"v": 7},
#     ...
#   },
#   ...
# }

# Extract: aqi = 152, pm25 = 152
```

### Step 4: Generate Timestamp

```python
from datetime import datetime

now = datetime.now()
# Format: yy/mm/dd hh:mm Week
weekday_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
timestamp = f"{now.strftime('%y/%m/%d %H:%M')} {weekday_names[now.weekday()]}"
# Example: "25/12/30 14:00 Mon"
```

### Step 5: Generate Warning Message (using LLM)

```python
# Use your LLM to generate a short health advice
prompt = f"Generate a short health advice (under 32 chars) for weather: {weather_desc}, {temp}°C and AQI: {aqi} ({pollution_level})."

warning_msg = await llm.generate(prompt)
# Example: "Sensitive groups wear masks!"
```

### Step 6: Format and Display

```python
# Prepare data according to WeatherDisplayInput schema
display_data = {
    "country_code": "CHN",  # Extract from aqi_result or weather_result
    "city_name": "Qingdao",
    "timestamp": timestamp,
    "weather_code": 63,  # From open-meteo
    "weather_desc": "Moderate Rain",  # From open-meteo
    "temperature": 7.0,  # From open-meteo
    "aqi": 152,  # From aqicn-air-quality
    "pm25": 152.0,  # From aqicn-air-quality
    "warning_msg": "Sensitive groups wear masks!"  # From LLM
}

# Call pi-sense-display MCP server
result = await mcp_client.call_tool(
    "pi-sense-display",
    "display_weather_info",
    display_data
)

# Expected response:
# "Successfully displayed weather for Qingdao. AQI: 152 (Moderate Rain, 7.0°C)"
```

## Complete Python Example

```python
import asyncio
from datetime import datetime
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def display_weather_for_city(city_name: str):
    """Complete workflow to display weather for a city."""
    
    # Initialize MCP clients
    async with stdio_client(StdioServerParameters(...)) as (read, write):
        async with ClientSession(read, write) as session:
            # 1. Get coordinates
            search_result = await session.call_tool(
                "open-meteo",
                "search_city",
                {"name": city_name}
            )
            # Parse lat/lon from result...
            
            # 2. Get weather
            weather_result = await session.call_tool(
                "open-meteo",
                "get_weather_forecast",
                {"latitude": lat, "longitude": lon}
            )
            # Parse weather data...
            
            # 3. Get AQI
            aqi_result = await session.call_tool(
                "aqicn-air-quality",
                "city_aqi",
                {"city": city_name}
            )
            # Parse AQI data...
            
            # 4. Generate timestamp
            now = datetime.now()
            weekday_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            timestamp = f"{now.strftime('%y/%m/%d %H:%M')} {weekday_names[now.weekday()]}"
            
            # 5. Generate warning (simplified - use your LLM)
            warning_msg = "Wear masks if sensitive!"
            
            # 6. Display
            display_result = await session.call_tool(
                "pi-sense-display",
                "display_weather_info",
                {
                    "country_code": "CHN",
                    "city_name": city_name,
                    "timestamp": timestamp,
                    "weather_code": weather_code,
                    "weather_desc": weather_desc,
                    "temperature": temperature,
                    "aqi": aqi,
                    "pm25": pm25,
                    "warning_msg": warning_msg
                }
            )
            
            print(display_result)

# Run
asyncio.run(display_weather_for_city("Qingdao"))
```

## Data Validation Notes

The `display_weather_info` tool performs strict validation:

- **Country Code**: Automatically uppercased, max 3 characters
- **City Name**: Trimmed whitespace
- **Temperature**: Float value (can be negative)
- **AQI**: Integer between 0 and 1000 (exclusive)
- **PM2.5**: Positive float (> 0)
- **Weather Code**: Should be valid WMO code (0-99 range typically)
- **Warning Message**: Maximum 32 characters including punctuation

If validation fails, the tool returns an error message describing the issue.

## Error Handling

All tools return error messages as strings when something goes wrong:

- **Validation errors**: Returned immediately with description
- **Hardware errors**: Logged and returned as error message
- **Missing resources**: Falls back to defaults when possible

Always check the return value for error messages before assuming success.

