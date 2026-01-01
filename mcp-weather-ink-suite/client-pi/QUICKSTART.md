# Quick Start Guide

## Prerequisites

- Python 3.8 or higher
- Raspberry Pi (for hardware) or development machine (for simulation)
- Waveshare 2.7" E-Paper Display (optional, for hardware mode)

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd project_root_mcp
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Waveshare EPD driver** (on Raspberry Pi only):
   ```bash
   # Follow Waveshare's installation instructions
   # Usually involves running their setup script or pip install
   ```

## Running the Server

### Basic Usage

```bash
python src/main.py
```

The server will start and listen for MCP client connections via stdio.

### MCP Configuration

Add this to your `mcp.json` (typically in `~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "pi-sense-display": {
      "command": "python",
      "args": [
        "D:\\work\\MCP_Severs\\project_root_mcp\\src\\main.py"
      ]
    }
  }
}
```

**For Raspberry Pi (SSH)**:
```json
{
  "mcpServers": {
    "pi-sense-display": {
      "command": "ssh",
      "args": [
        "alex@192.168.3.13",
        "/home/alex/ProjectVenv/bin/python",
        "/home/alex/ProjectVenv/MCP_Sever_Practice/project_root_mcp/src/main.py"
      ]
    }
  }
}
```

## Testing the Tool

### Using MCP Client

```python
from mcp import ClientSession

async def test_display():
    # ... initialize MCP client ...
    
    result = await session.call_tool(
        "pi-sense-display",
        "display_weather_info",
        {
            "country_code": "CHN",
            "city_name": "Qingdao",
            "timestamp": "25/12/30 14:00 Mon",
            "weather_code": 63,
            "weather_desc": "Moderate Rain",
            "temperature": 7.0,
            "aqi": 152,
            "pm25": 152.0,
            "warning_msg": "Wear masks if sensitive!"
        }
    )
    print(result)
```

### Expected Output

**Success**:
```
Successfully displayed weather for Qingdao. AQI: 152 (Moderate Rain, 7.0°C)
```

**Validation Error**:
```
Validation error: AQI must be between 0 and 1000 (got 1500)
```

## Simulation Mode

If the Waveshare EPD driver is not installed, the server runs in **simulation mode**:
- No hardware interaction
- Debug images saved to disk:
  - `debug_sim_black.png`
  - `debug_sim_red.png`
  - `debug_rgb_display.png`
  - `debug_black_display.png`
  - `debug_red_display.png`

Check these images to verify the display would look correct.

## Troubleshooting

### Import Errors

If you see `ModuleNotFoundError`:
```bash
# Make sure you're in the project_root_mcp directory
# Or install in development mode:
pip install -e .
```

### Hardware Not Found

If you see "Waveshare EPD driver not found":
- This is normal on non-Raspberry Pi machines
- Server will run in simulation mode
- Debug images will be saved instead

### Path Issues

If resources (icons, fonts) are not found:
- Check that `src/resources/` contains:
  - `weather_type/` folder with PNG files
  - `emoticon_30px/` folder with PNG files
  - `Righteous-Regular.ttf` font file

### Validation Errors

If you get validation errors:
- Check that AQI is between 0 and 1000 (exclusive)
- Check that PM2.5 is positive (> 0)
- Check that warning message is 32 characters or less
- Check that country code is 3 characters or less

## Next Steps

1. **Integrate with other MCP servers**: See `USAGE_EXAMPLE.md`
2. **Customize display**: Modify `src/services/drawing.py`
3. **Add features**: Extend `src/tools/display.py`

## Support

For detailed documentation:
- `README.md`: Full project documentation
- `USAGE_EXAMPLE.md`: Integration examples
- `PROJECT_SUMMARY.md`: Refactoring details

