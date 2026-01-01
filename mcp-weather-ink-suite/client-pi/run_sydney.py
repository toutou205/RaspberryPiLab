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
    # Hardcoded Sydney Data from previous fetch
    data = {
        "country_code": "AUS",
        "city_name": "Sydney",
        "timestamp": "25/12/31 20:30 Wed",
        "weather_code": 3,
        "weather_desc": "Overcast",
        "temperature": 19.3,
        "aqi": 23,
        "pm25": 23.0,
        "advice_msg": "Breathe easy, stay active!"
    }
    
    print("--- Displaying Sydney Weather ---")
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
