import asyncio
import logging
import sys
import os

# Configure logging to see debug output from EPD driver
logging.basicConfig(level=logging.DEBUG)

# Add 'src' to sys.path so that imports within src (like 'from services...') work correctly
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.tools.display import WeatherDisplayInput
from src.services.hardware import EPDService
from src.services.drawing import generate_weather_image, split_image_for_epd

# Simulate the Display Tool Logic
async def test_display():
    print("--- Sending Test Data to E-Ink Display ---")
    
    # Constructed payload
    test_data = {
        "country_code": "CHN",
        "city_name": "TestCity",
        "timestamp": "25/01/01 12:00 Wed",
        "weather_code": 1, # Mainly Clear
        "weather_desc": "Mainly Clear",
        "temperature": 25.5,
        "aqi": 55,
        "pm25": 12.0,
        "advice_msg": "Test Display: Hello World!"
    }
    
    try:
        # 1. Validation
        print(f"Validating input: {test_data}")
        input_model = WeatherDisplayInput(**test_data)
        
        # 2. Draw Image (Local Test)
        print("Generating image...")
        rgb_image = generate_weather_image(input_model.model_dump())
        rgb_image.save("test_output_rgb.png")
        print("Saved 'test_output_rgb.png' for inspection.")
        
        # 3. Hardware Display (Mock if not on Pi, Real if on Pi)
        # Note: If running on Windows, EPDService likely mocks hardware via simulate_display logic 
        # provided it's set up that way, or we can just skip hardware call if import fails.
        try:
            print("Attempting to access hardware/simulator...")
            epd = EPDService()
            black, red = split_image_for_epd(rgb_image)
            epd.display(black, red)
            print("Display command sent successfully.")
        except Exception as hw_e:
            print(f"Hardware display skipped or failed: {hw_e}")
            print("(This is expected if running on Windows without SPI)")

    except Exception as e:
        print(f"Test Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_display())
