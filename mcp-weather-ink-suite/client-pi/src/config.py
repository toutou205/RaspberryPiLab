"""
Configuration management for the MCP Server.
Handles environment variables, paths, and constants.
"""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # E-Paper Display Configuration
    EPD_WIDTH: int = 264
    EPD_HEIGHT: int = 176
    
    # Resource Paths (relative to src/resources)
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RESOURCE_DIR: str = os.path.join(BASE_DIR, "src", "resources")
    
    FONT_NAME: str = "Righteous-Regular.ttf"
    PATH_EMOTICON: str = "emoticon_30px"
    PATH_WEATHER: str = "weather_type"

    @property
    def font_path(self) -> str:
        """Get the full path to the font file."""
        return os.path.join(self.RESOURCE_DIR, self.FONT_NAME)

    @property
    def emoticon_dir(self) -> str:
        """Get the full path to the emoticon directory."""
        return os.path.join(self.RESOURCE_DIR, self.PATH_EMOTICON)

    @property
    def weather_dir(self) -> str:
        """Get the full path to the weather icons directory."""
        return os.path.join(self.RESOURCE_DIR, self.PATH_WEATHER)

    # Color Definitions (RGB tuples)
    COLOR_BLACK: tuple = (0, 0, 0)
    COLOR_WHITE: tuple = (255, 255, 255)
    COLOR_RED: tuple = (255, 0, 0)

    class Config:
        """Pydantic configuration."""
        case_sensitive = False


# Global settings instance
settings = Settings()

