import sys
import json
import logging
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Add 'src' to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.tools.display import WeatherDisplayInput
from src.services.hardware import EPDService
from src.services.drawing import generate_weather_image, split_image_for_epd

def display_from_json(json_str):
    print(f"Received Payload: {json_str}")
    try:
        data = json.loads(json_str)
        # Validate using Pydantic model
        input_model = WeatherDisplayInput(**data)
        
        # Generate Image
        print("Generating image...")
        rgb_image = generate_weather_image(input_model.model_dump())
        
        # Display on Hardware
        print("Displaying on E-Ink...")
        epd = EPDService()
        black, red = split_image_for_epd(rgb_image)
        epd.display(black, red)
        print("SUCCESS: Image sent to display.")
        
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python display_json.py '<json_string>'")
        sys.exit(1)
    
    display_from_json(sys.argv[1])
