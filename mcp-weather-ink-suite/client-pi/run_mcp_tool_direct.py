import sys
import os
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Fix path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.server import create_server

async def main():
    print("--- Debugging MCP Tool Direct Execution ---")
    try:
        # Create the server instance (this runs register_tools)
        mcp = create_server()
        print("MCP Server created.")
        
        # Hanoi Data
        args = {
            "country_code": "VNM",
            "city_name": "Hanoi",
            "timestamp": "25/12/31 18:16 Wed",
            "weather_code": 3,
            "weather_desc": "Overcast",
            "temperature": 22.7,
            "aqi": 81,
            "pm25": 81.0,
            "advice_msg": "Breathe easy, stay active!"
        }
        
        print(f"Calling tool 'display_weather_info' with args: {args}")
        
        # FastMCP doesn't verified expose a simple public 'call_tool' method for local debug 
        # easily without running the server loop, but we can access the tool function directly 
        # if we know how FastMCP stores it, or we can just import the underlying function content 
        # if we want to test logic. 
        # However, to test the REGISTRATION, we should try to invoke it via the server if possible.
        # Looking at FastMCP source (assumed), it likely has a registry.
        
        # reliable fallback: Import the function logic directly to simple-test 
        # BUT user wants MCP integration proof.
        # Let's try to use the mcp object if it has a way, otherwise fallback to direct logic.
        
        # Accessing the internal tool list to find the function
        # mcp._tool_manager.list_tools() ... invalid assumption without seeing FastMCP code.
        
        # ALTERNATIVE: Use the transport loop with a pipe in python? No, too complex.
        
        # Let's import the register function and verify we can run the decorated function.
        # In `src/tools/display.py`, `register_tools` defines the function inside. 
        # It's not globally available. 
        # We need to rely on `create_server` returning an object we can inspect.
        
        # HACK: We will try to run the `call_tool` implementation if it exists, 
        # or just inspect `mcp` dir.
        
        # Actually, for "One Click" we need the SERVER to work.
        # Let's run the server in a separate thread/process and feed it stdin?
        # A simpler first step: Just verify the `drawing.py` fix worked by running the generation logic manually 
        # but with the exact imports the server uses.
        
        from src.tools.display import WeatherDisplayInput
        from src.services.drawing import generate_weather_image, split_image_for_epd
        from src.services.hardware import EPDService
        
        print("Validating Input model...")
        input_data = WeatherDisplayInput(**args)
        
        print("Generating Image (Checking drawing.py)...")
        rgb = generate_weather_image(input_data.model_dump())
        
        print("Initializing Hardware...")
        epd = EPDService()
        
        print("Displaying...")
        black, red = split_image_for_epd(rgb)
        epd.display(black, red)
        print("SUCCESS: Tool Logic Executed Manually.")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
