from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# 数据定义层：存放 Pydantic BaseModel (Payload & API Response)

class EInkPayload(BaseModel):
    """
    Schema for the data sent to the Raspberry Pi e-ink display.
    """
    country_code: str = Field(..., description="Country code (e.g., 'USA', 'CHN')", max_length=3)
    city_name: str = Field(..., description="Name of the city")
    timestamp: str = Field(..., description="Formatted timestamp: YY/MM/DD HH:mm Week", pattern=r"^\d{2}/\d{2}/\d{2} \d{2}:\d{2} (Mon|Tue|Wed|Thu|Fri|Sat|Sun)$")
    weather_code: int = Field(..., description="WMO weather code", ge=0, le=99)
    weather_desc: str = Field(..., description="Weather description in English")
    temperature: float = Field(..., description="Temperature in Celsius")
    aqi: int = Field(..., description="Air Quality Index", ge=0, le=1000)
    pm25: float = Field(..., description="PM2.5 concentration", ge=0)
    advice_msg: str = Field(..., description="Witty health advice based on WHO standards (Temp & AQI). Style: Humorous but practical. Constraint: Max 32 chars including spaces/punctuation.", max_length=32)

class WeatherData(BaseModel):
    temperature: float
    weather_code: int
    wind_speed: float
    timezone: str
    utc_offset_seconds: int

class AirQualityData(BaseModel):
    aqi: int
    pm25: float
