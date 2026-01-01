# Pi-Sense-Display MCP Server

MCP Server for Raspberry Pi E-Ink Weather Display Terminal. This server provides a tool interface for displaying weather and air quality information on a Waveshare 2.7" E-Paper display.

## Project Structure

```
project_root_mcp/
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── src/
    ├── __init__.py
    ├── main.py               # Entry point
    ├── config.py            # Configuration management
    ├── server.py            # MCP Server initialization
    ├── resources/           # Static resources
    │   ├── weather_type/    # Weather icons
    │   ├── emoticon_30px/   # AQI emoticons
    │   └── Righteous-Regular.ttf  # Font file
    ├── services/            # Core business logic
    │   ├── __init__.py
    │   ├── hardware.py      # E-Paper hardware abstraction
    │   └── drawing.py       # Image generation logic
    └── tools/               # MCP Tool implementations
        ├── __init__.py
        └── display.py       # Weather display tool
```

## Features

- **Modular Architecture**: Clean separation of concerns (hardware, drawing, MCP tools)
- **Data Validation**: Pydantic models ensure data integrity
- **Hardware Abstraction**: Graceful degradation when hardware is unavailable (simulation mode)
- **Three-Tier AQI Display**: Color-coded interface based on air quality levels
- **WMO Weather Code Support**: Maps Open-Meteo WMO codes to local weather icons

## Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Waveshare EPD driver** (on Raspberry Pi):
   ```bash
   # Follow Waveshare's installation instructions for your display model
   # The driver should be installed via pip or their setup script
   ```

## Usage

### Running the Server

```bash
python src/main.py
```

The server will start and listen for MCP client connections.

### MCP Tool: `display_weather_info`

**Input Schema**:
```json
{
  "country_code": "CHN",           // ISO country code (max 3 chars)
  "city_name": "Chongqing",        // City name
  "timestamp": "25/12/29 13:00 Mon", // Formatted timestamp
  "weather_code": 63,              // WMO weather code (from Open-Meteo)
  "weather_desc": "Moderate Rain", // Weather description
  "temperature": 11.0,             // Temperature in Celsius
  "aqi": 152,                      // Air Quality Index (0-1000)
  "pm25": 53.0,                    // PM2.5 concentration (>0)
  "warning_msg": "Wear masks!"     // Health advice (max 32 chars)
}
```

**Validation Rules**:
- `country_code`: Maximum 3 characters, auto-uppercased
- `city_name`: Required, trimmed
- `temperature`: Float value
- `aqi`: Integer between 0 and 1000
- `pm25`: Positive float
- `weather_code`: Must be valid WMO code (falls back to "Unknown" icon if not mapped)
- `warning_msg`: Maximum 32 characters including punctuation

**Example Response**:
```
Successfully displayed weather for Chongqing. AQI: 152 (Moderate Rain, 11.0°C)
```

## Display Color Scheme

The display uses a three-tier color scheme based on AQI:

1. **Normal (AQI 0-100)**: White background, black text
2. **Warning (AQI 101-200)**: White background, red highlights
3. **Alert (AQI >200)**: Red background, white text

## WMO Weather Code Mapping

The server maps Open-Meteo WMO codes to local weather icons:

| WMO Code | Icon File | Description |
|----------|-----------|-------------|
| 0 | 100.png | Clear sky |
| 1 | 102.png | Mainly clear |
| 2 | 103.png | Partly cloudy |
| 3 | 104.png | Overcast |
| 45 | 501.png | Fog |
| 48 | 510.png | Rime fog |
| 61 | 305.png | Light rain |
| 63 | 306.png | Moderate rain |
| 65 | 307.png | Heavy rain |
| ... | ... | ... |

See `src/services/drawing.py` for the complete mapping table.

## Development Mode

When the Waveshare EPD driver is not available (e.g., on a development machine), the server runs in **simulation mode**:
- Display operations are logged but not executed
- Debug images are saved to disk (`debug_sim_black.png`, `debug_sim_red.png`)

## Integration with Other MCP Servers

This server is designed to work with:
- **open-meteo**: Provides weather data and WMO codes
- **aqicn-air-quality**: Provides AQI and PM2.5 data

A typical workflow:
1. Query `open-meteo` for weather data (including WMO code)
2. Query `aqicn-air-quality` for air quality data
3. Format data according to `WeatherDisplayInput` schema
4. Call `display_weather_info` tool to render on display

## Error Handling

- **Validation Errors**: Returned as error messages in tool response
- **Hardware Errors**: Logged with full stack trace
- **Missing Resources**: Falls back to default icons/fonts when possible

## License

[Add your license here]

## Author

Refactored from `main_rpi_aqi_levels.py` to production-grade MCP Server architecture.

