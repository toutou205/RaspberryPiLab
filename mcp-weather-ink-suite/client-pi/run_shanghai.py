import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.tools.display import WeatherDisplayInput
from src.services.hardware import EPDService
from src.services.drawing import generate_weather_image, split_image_for_epd

def main():
    # Hardcoded Shanghai Data
    data = {
        "country_code": "CHN",
        "city_name": "Shanghai",
        "timestamp": "25/12/31 18:00 Wed",
        "weather_code": 3,
        "weather_desc": "Overcast",
        "temperature": 7.3,
        "aqi": 43,
        "pm25": 12.0,
        "advice_msg": "Dress warm! Air's good, walk!"
    }
    
    print("--- Displaying Shanghai Weather ---")
    try:
        input_model = WeatherDisplayInput(**data)
        
        print("Generating image...")
        rgb_image = generate_weather_image(input_model.model_dump())
        
        print("Initializing EPD...")
        epd = EPDService()
        
        print("Splitting image...")
        black, red = split_image_for_epd(rgb_image)
        
        print("Sending to display...")
        epd.display(black, red)
        print("SUCCESS: Display update command finished.")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
