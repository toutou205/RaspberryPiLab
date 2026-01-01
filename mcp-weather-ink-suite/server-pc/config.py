import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class: Reads environment variables and defines constant mappings."""
    AQICN_API_KEY = os.getenv("AQICN_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    ADVICE_MODE = os.getenv("ADVICE_MODE", "API") # API or SAMPLING
    
    # Raspberry Pi Configuration
    PI_HOST = os.getenv("PI_HOST", "raspberrypi.local")
    PI_USER = os.getenv("PI_USER", "pi")
    HTTPS_PROXY = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")
    HTTP_PROXY = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")

    # Mapping for country codes (Using a simplified map for reference, real implementation might use a library or extensive list)
    # The requirement says "Introduce conversion logic (or use pycountry library)".
    # For now, we will use the map from weather_only.py as a base.
    COUNTRY_CODES = {
        "Italy": "ITA",
        "China": "CHN",
        "United States": "USA",
        "United Kingdom": "GBR",
        "France": "FRA",
        "Germany": "DEU",
        "Spain": "ESP",
        "Japan": "JPN",
        "South Korea": "KOR",
        "India": "IND",
        "Brazil": "BRA",
        "Canada": "CAN",
        "Australia": "AUS",
        "Russia": "RUS",
        "Mexico": "MEX",
        "Netherlands": "NLD",
        "Belgium": "BEL",
        "Switzerland": "CHE",
        "Austria": "AUT",
        "Sweden": "SWE",
        "Norway": "NOR",
        "Denmark": "DNK",
        "Finland": "FIN",
        "Poland": "POL",
        "Portugal": "PRT",
        "Greece": "GRC",
        "Turkey": "TUR",
        "Thailand": "THA",
        "Singapore": "SGP",
        "Malaysia": "MYS",
        "Indonesia": "IDN",
        "Philippines": "PHL",
        "Vietnam": "VNM",
        "New Zealand": "NZL",
        "South Africa": "ZAF",
        "Argentina": "ARG",
        "Chile": "CHL",
        "Colombia": "COL",
        "Peru": "PER",
        "Egypt": "EGY",
        "Saudi Arabia": "SAU",
        "United Arab Emirates": "ARE",
        "Israel": "ISR",
        "Ireland": "IRL",
        "Czech Republic": "CZE",
        "Hungary": "HUN",
        "Romania": "ROU",
        "Bulgaria": "BGR",
        "Croatia": "HRV",
        "Serbia": "SRB",
        "Slovakia": "SVK",
        "Slovenia": "SVN",
        "Ukraine": "UKR",
        "Belarus": "BLR",
        "Kazakhstan": "KAZ",
        "Uzbekistan": "UZB",
        "Iraq": "IRQ",
        "Iran": "IRN",
        "Pakistan": "PAK",
        "Bangladesh": "BGD",
        "Sri Lanka": "LKA",
        "Myanmar": "MMR",
        "Cambodia": "KHM",
        "Laos": "LAO",
        "Mongolia": "MNG",
        "Nepal": "NPL",
        "Bhutan": "BTN",
        "Afghanistan": "AFG",
        "Yemen": "YEM",
        "Oman": "OMN",
        "Kuwait": "KWT",
        "Qatar": "QAT",
        "Bahrain": "BHR",
        "Jordan": "JOR",
        "Lebanon": "LBN",
        "Syria": "SYR",
        "Iceland": "ISL",
        "Luxembourg": "LUX",
        "Malta": "MLT",
        "Cyprus": "CYP",
        "Estonia": "EST",
        "Latvia": "LVA",
        "Lithuania": "LTU",
        "Moldova": "MDA",
        "Albania": "ALB",
        "Bosnia and Herzegovina": "BIH",
        "North Macedonia": "MKD",
        "Montenegro": "MNE",
        "Kosovo": "XKX",
        "Georgia": "GEO",
        "Armenia": "ARM",
        "Azerbaijan": "AZE",
    }
