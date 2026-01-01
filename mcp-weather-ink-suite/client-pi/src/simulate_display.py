import sys
import os
import logging
from datetime import datetime
from typing import List, Dict

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("simulate_display")

# Ensure we can import from the current directory (src)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from services.drawing import generate_weather_image, split_image_for_epd
    from config import settings
except ImportError as e:
    logger.error(f"Import failed: {e}")
    logger.info(f"sys.path: {sys.path}")
    raise

def run_simulation_case(case_name: str, data: Dict):
    logger.info(f"--- Simulating Case: {case_name} ---")
    logger.info(f"Data: {data}")
    
    # 1. Generate RGB Image
    try:
        rgb_image = generate_weather_image(data)
        rgb_filename = f"simulation_{case_name}_rgb.png"
        rgb_image.save(rgb_filename)
        logger.info(f"Saved RGB: {rgb_filename}")
    except Exception as e:
        logger.error(f"Failed to generate RGB image for {case_name}: {e}")
        return

    # 2. Split for EPD
    try:
        image_black, image_red = split_image_for_epd(rgb_image)
        
        black_filename = f"simulation_{case_name}_black.png"
        red_filename = f"simulation_{case_name}_red.png"
        
        image_black.save(black_filename)
        image_red.save(red_filename)
        
        logger.info(f"Saved Black Channel: {black_filename}")
        logger.info(f"Saved Red Channel: {red_filename}")
        
    except Exception as e:
        logger.error(f"Failed to split image for {case_name}: {e}")

def simulate():
    logger.info("Starting simulation...")
    
    # Test Case 1: Rome (User provided)
    # Note: User provided 'city' key, mapped to 'city_name'
    # Added 'country_code' default
    case_rome = {
        "country_code": "IT", 
        "city_name": "Rome",
        "timestamp": "25/12/30 15:00 Tue",
        "weather_code": 1,
        "weather_desc": "Mainly clear",
        "temperature": 13.1,
        "aqi": 104,
        "pm25": 104,
        "warning_msg": "Wear mask & warm clothes!"
    }

    # Test Case 2: Yogyakarta (User provided)
    case_yogya = {
        "country_code": "IDN",
        "city_name": "Yogyakarta",
        "timestamp": "25/12/30 01:00 Mon",
        "weather_code": 2,
        "weather_desc": "Partly cloudy",
        "temperature": 27.5,
        "aqi": 90,
        "pm25": 90.0,
        "warning_msg": "Sensitive people take care!"
    }
    
    run_simulation_case("rome", case_rome)
    run_simulation_case("yogyakarta", case_yogya)
    
    logger.info("All simulations complete.")

if __name__ == "__main__":
    simulate()
