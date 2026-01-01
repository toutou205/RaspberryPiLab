"""
Hardware abstraction layer for E-Paper Display.
Handles interaction with Waveshare EPD driver.
"""
import logging
from PIL import Image
from typing import Optional

# # Try to import Waveshare EPD driver
# try:
#     from waveshare_epd import epd2in7b
#     HAS_EPD = True
# except ImportError:
#     HAS_EPD = False
#     logging.warning("Waveshare EPD driver not found. Running in simulation mode.")
    
# Try to import Waveshare EPD driver, catching any exception during driver init
import traceback
try:
    import epd2in7b
    HAS_EPD = True
    logging.debug("epd2in7b imported successfully in hardware.py")
except Exception as e:
    HAS_EPD = False
    logging.debug(f"epd2in7b import FAILED: {e}")
    logging.warning(f"Waveshare EPD driver unavailable ({e}). Running in simulation mode.")


class EPDService:
    """
    Service for managing E-Paper Display hardware.
    
    Provides abstraction over the Waveshare EPD driver, allowing
    graceful degradation when hardware is not available (e.g., during development).
    """
    
    def __init__(self):
        """Initialize the EPD service."""
        self.logger = logging.getLogger(__name__)
        self.epd: Optional[object] = None
        
        if HAS_EPD:
            try:
                self.epd = epd2in7b.EPD()
                self.logger.info("EPD driver initialized successfully.")
            except Exception as e:
                self.logger.error(f"Failed to initialize EPD driver: {e}")
                self.epd = None
        else:
            self.logger.info("Running in simulation mode (no hardware).")

    def display(self, image_black: Image.Image, image_red: Image.Image) -> None:
        """
        Display images on the E-Paper screen.
        
        Args:
            image_black: Black channel image (1-bit)
            image_red: Red channel image (1-bit)
            
        Raises:
            IOError: If hardware communication fails
        """
        if not HAS_EPD or self.epd is None:
            self.logger.info("Simulation: Display update requested.")
            # Save debug images for development
            try:
                image_black.save("debug_sim_black.png")
                image_red.save("debug_sim_red.png")
                self.logger.info("Debug images saved: debug_sim_black.png, debug_sim_red.png")
            except Exception as e:
                self.logger.warning(f"Failed to save debug images: {e}")
            return

        try:
            self.logger.info("Initializing EPD hardware...")
            self.epd.init()
            # Optional: Clear screen before display
            # self.epd.Clear()

            self.logger.info("Sending buffer to display (this may take 10-15 seconds)...")
            self.epd.display(
                self.epd.getbuffer(image_black),
                self.epd.getbuffer(image_red)
            )
            
            self.logger.info("Display update complete. Entering sleep mode.")
            self.epd.sleep()
            
        except IOError as e:
            self.logger.error(f"Hardware IO error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected hardware error: {e}")
            raise
