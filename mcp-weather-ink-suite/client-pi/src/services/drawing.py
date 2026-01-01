"""
Drawing and image generation service.
Contains all logic for creating the weather display interface.
"""
import os
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Tuple
from config import settings

# WMO Weather Code to Icon File Mapping
# Maps Open-Meteo WMO codes to local icon filenames
WMO_MAPPING = {
    0: "100.png",      # Clear sky
    1: "102.png",      # Mainly clear
    2: "103.png",      # Partly cloudy
    3: "104.png",      # Overcast
    45: "501.png",     # Fog
    48: "510.png",     # Depositing rime fog
    51: "309.png",     # Light drizzle
    53: "309.png",     # Moderate drizzle
    55: "309.png",     # Dense drizzle
    56: "313.png",     # Light freezing drizzle
    57: "313.png",     # Dense freezing drizzle
    61: "305.png",     # Slight rain
    63: "306.png",     # Moderate rain
    65: "307.png",     # Heavy rain
    66: "313.png",     # Light freezing rain
    67: "313.png",     # Heavy freezing rain
    71: "400.png",     # Slight snow fall
    73: "401.png",     # Moderate snow fall
    75: "402.png",     # Heavy snow fall
    77: "400.png",     # Snow grains
    80: "300.png",     # Slight rain showers
    81: "300.png",     # Moderate rain showers
    82: "301.png",     # Violent rain showers
    85: "407.png",     # Slight snow showers
    86: "407.png",     # Heavy snow showers
    95: "302.png",     # Thunderstorm
    96: "304.png",     # Thunderstorm with slight hail
    99: "304.png",     # Thunderstorm with heavy hail
}


def load_font(size: int) -> ImageFont.FreeTypeFont:
    """
    Load font with specified size.
    
    Args:
        size: Font size in points
        
    Returns:
        Font object (falls back to default if custom font not found)
    """
    try:
        return ImageFont.truetype(settings.font_path, size)
    except IOError:
        return ImageFont.load_default()


def sanitize_text(text: str) -> str:
    """
    Sanitize text for display compatibility.
    
    Replaces problematic characters that may not render correctly.
    
    Args:
        text: Input text (will be converted to string if not already)
        
    Returns:
        Sanitized text string
    """
    if not isinstance(text, str):
        text = str(text)
    return text.replace("℃", "°C").replace("μ", "u").replace("！", "!").replace("：", ":")


def recolor_icon(icon_path: str, target_color: Tuple[int, int, int]) -> Image.Image:
    """
    Load an icon and recolor it to the target color.
    
    Args:
        icon_path: Full path to the icon file
        target_color: RGB tuple for target color
        
    Returns:
        RGBA Image with recolored icon (transparent background)
    """
    if not os.path.exists(icon_path):
        return Image.new("RGBA", (20, 20), (0, 0, 0, 0))
    
    icon = Image.open(icon_path).convert("RGBA")
    color_block = Image.new("RGBA", icon.size, target_color)
    result = Image.new("RGBA", icon.size, (0, 0, 0, 0))
    result.paste(color_block, (0, 0), mask=icon)
    return result


def draw_text_centered_x(
    draw: ImageDraw.Draw,
    text: str,
    font: ImageFont.FreeTypeFont,
    y: int,
    center_x: int,
    color: Tuple[int, int, int]
) -> None:
    """
    Draw text centered horizontally at specified y position.
    
    Args:
        draw: PIL ImageDraw object
        text: Text to draw
        font: Font to use
        y: Y coordinate
        center_x: X coordinate for center alignment
        color: Text color (RGB tuple)
    """
    text = sanitize_text(text)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    draw.text((center_x - text_width / 2, y), text, font=font, fill=color)


def draw_text_absolute(
    draw: ImageDraw.Draw,
    text: str,
    font: ImageFont.FreeTypeFont,
    x: int,
    y: int,
    color: Tuple[int, int, int] = (0, 0, 0)
) -> None:
    """
    Draw text at absolute coordinates.
    
    Args:
        draw: PIL ImageDraw object
        text: Text to draw
        font: Font to use
        x: X coordinate
        y: Y coordinate
        color: Text color (RGB tuple)
    """
    text = sanitize_text(text)
    draw.text((x, y), text, font=font, fill=color)


def get_aqi_icon_and_level(aqi: int) -> Tuple[str, str]:
    """
    Get emoticon filename and pollution level text based on AQI value.
    
    Args:
        aqi: Air Quality Index value
        
    Returns:
        Tuple of (emoticon_filename, pollution_level_text)
    """
    if 0 <= aqi <= 50:
        return "emoticon-happy-outline.png", "Good"
    elif 51 <= aqi <= 100:
        return "emoticon-neutral-outline.png", "Moderate"
    elif 101 <= aqi <= 150:
        return "emoticon-sad-outline.png", "Unhealthy\nfor Sensitive Groups"
    elif 151 <= aqi <= 200:
        return "emoticon-cry-outline.png", "Unhealthy"
    elif 201 <= aqi <= 300:
        return "emoticon-sick-outline.png", "Very Unhealthy"
    else:
        return "emoticon-dead-outline.png", "Hazardous"


def split_image_for_epd(rgb_image: Image.Image) -> Tuple[Image.Image, Image.Image]:
    """
    Convert RGB image to black and red channel bitmaps for E-Paper display.
    
    Uses improved conversion logic:
    - Red detection: R > 200, G < 80, B < 80 -> Red channel
    - Black detection: Grayscale < 128 -> Black channel
    - White: Everything else
    
    Args:
        rgb_image: Input RGB PIL Image
        
    Returns:
        Tuple of (black_channel_image, red_channel_image) - both 1-bit images
    """
    width, height = rgb_image.size
    image_black = Image.new('1', (width, height), 255)
    image_red = Image.new('1', (width, height), 255)

    gray_image = rgb_image.convert('L')
    pixels = rgb_image.load()
    pixels_gray = gray_image.load()
    pixels_b = image_black.load()
    pixels_r = image_red.load()

    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            gray = pixels_gray[x, y]

            # Red detection
            if r > 200 and g < 80 and b < 80:
                pixels_r[x, y] = 0  # Red pixel
                pixels_b[x, y] = 1  # White in black channel
            # Black detection
            elif gray < 128:
                pixels_b[x, y] = 0  # Black pixel
                pixels_r[x, y] = 1  # White in red channel
            # White
            else:
                pixels_b[x, y] = 1  # White
                pixels_r[x, y] = 1  # White

    return image_black, image_red


def generate_weather_image(data: Dict) -> Image.Image:
    """
    Generate the complete weather display interface as an RGB image.
    
    Implements three-tier AQI color scheme:
    1. 0-100: White background, black text (normal)
    2. 101-200: White background, red highlights (warning)
    3. >200: Red background, white text (alert)
    
    Args:
        data: Dictionary containing display data with keys:
            - country_code: ISO country code (e.g., "CHN")
            - city_name: City name (e.g., "Chongqing")
            - timestamp: Formatted timestamp string
            - weather_code: WMO weather code (integer)
            - weather_desc: Weather description text
            - temperature: Temperature value (float or string)
            - aqi: Air Quality Index (integer)
            - pm25: PM2.5 concentration value
            - advice_msg: Health advice message (max 32 chars)
            
    Returns:
        RGB PIL Image ready for display
    """
    image = Image.new("RGB", (settings.EPD_WIDTH, settings.EPD_HEIGHT), settings.COLOR_WHITE)
    draw = ImageDraw.Draw(image)

    # Load fonts
    fonts = {
        13: load_font(13),
        14: load_font(14),
        15: load_font(15),
        16: load_font(16),
        20: load_font(20),
        48: load_font(48)
    }

    # 1. Top bar
    draw.rectangle([(0, 0), (settings.EPD_WIDTH, 24)], fill=settings.COLOR_BLACK)
    draw_text_centered_x(
        draw, "Smart Weather Display Terminal",
        fonts[14], 5, settings.EPD_WIDTH / 2, settings.COLOR_WHITE
    )

    # 2. Info bar (Country/City/Time)
    y_bc = 24
    mid_x = settings.EPD_WIDTH // 2
    draw_text_centered_x(
        draw, f"{data['country_code']}-{data['city_name']}",
        fonts[14], y_bc + 2, mid_x / 2, settings.COLOR_BLACK
    )
    draw_text_absolute(
        draw, data['timestamp'],
        fonts[14], mid_x - 4, y_bc + 2, settings.COLOR_BLACK
    )

    # 3. Core area (AQI & Weather)
    y_de = 44
    aqi_val = int(data['aqi'])
    
    # Three-tier color scheme
    if aqi_val <= 100:
        bg_color = settings.COLOR_WHITE
        fg_color = settings.COLOR_BLACK
        highlight_color = settings.COLOR_BLACK
        icon_color = settings.COLOR_BLACK
    elif 101 <= aqi_val <= 200:
        bg_color = settings.COLOR_WHITE
        fg_color = settings.COLOR_BLACK
        highlight_color = settings.COLOR_RED
        icon_color = settings.COLOR_RED
    else:  # aqi_val > 200
        bg_color = settings.COLOR_RED
        fg_color = settings.COLOR_WHITE
        highlight_color = settings.COLOR_WHITE
        icon_color = settings.COLOR_WHITE

    draw.rectangle([(0, y_de), (settings.EPD_WIDTH, y_de + 104)], fill=bg_color)

    # Weather icon
    w_filename = WMO_MAPPING.get(data['weather_code'], "999.png")
    w_path = os.path.join(settings.weather_dir, w_filename)
    w_img = recolor_icon(w_path, icon_color).resize((60, 60), Image.Resampling.LANCZOS)
    image.paste(w_img, (36, 62), mask=w_img)

    # Emoticon icon
    emo_file, pollution_text = get_aqi_icon_and_level(aqi_val)
    emo_path = os.path.join(settings.emoticon_dir, emo_file)
    emo_img = recolor_icon(emo_path, icon_color).resize((24, 24), Image.Resampling.LANCZOS)
    image.paste(emo_img, (5, 49), mask=emo_img)

    # Text elements
    temp_str = str(data['temperature']).replace('.0', '') if isinstance(data['temperature'], float) else str(data['temperature'])
    weather_str = f"{data['weather_desc']} {temp_str}°C"
    draw_text_centered_x(draw, weather_str, fonts[15], 130, 66, fg_color)

    draw_text_absolute(draw, "PM2.5:", fonts[13], 136, 48, fg_color)
    pm25_str = str(data['pm25']).replace('.0', '') if isinstance(data['pm25'], float) else str(data['pm25'])
    draw_text_absolute(draw, f"   {pm25_str} ug/m3", fonts[13], 171, 48, fg_color)
    draw_text_absolute(draw, "AQI", fonts[20], 132, 70, fg_color)
    
    # AQI value uses highlight color
    draw_text_absolute(draw, str(aqi_val), fonts[48], 171, 60, highlight_color)

    # Pollution level text
    if '\n' in pollution_text:
        lines = pollution_text.split('\n')
        draw_text_centered_x(draw, lines[0], fonts[13], 119, 132 + 66, fg_color)
        draw_text_centered_x(draw, lines[1], fonts[13], 131, 132 + 66, fg_color)
    else:
        draw_text_centered_x(draw, pollution_text, fonts[16], 119, 132 + 66, fg_color)

    # 4. Bottom advice message (LLM-generated)
    draw.rectangle([(0, 148), (settings.EPD_WIDTH, 176)], fill=settings.COLOR_WHITE)
    draw.line([(0, 148), (settings.EPD_WIDTH, 148)], fill=settings.COLOR_BLACK, width=1)
    draw_text_centered_x(
        draw, data['advice_msg'],
        fonts[16], 153, settings.EPD_WIDTH / 2, settings.COLOR_BLACK
    )

    return image

