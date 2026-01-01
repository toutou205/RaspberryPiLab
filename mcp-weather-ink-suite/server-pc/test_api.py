import asyncio
import traceback
from services.processor import process_logic
from services.advisor import get_advisor
from utils.validator import validate_payload
from mcp.server.fastmcp import Context

# Mock Data
MOCK_GEO = {
    "latitude": 51.5074,
    "longitude": -0.1278,
    "country_code": "GBR",
    "city_name": "London",
    "timezone": "Europe/London"
}

MOCK_WEATHER = {
    "temperature": 15.5,
    "weather_code": 3, # Overcast
    "wind_speed": 10.0,
    "timezone": "Europe/London",
    "utc_offset_seconds": 0
}

MOCK_AQI = {
    "aqi": 42,
    "pm25": 12.5
}

# Mock Context for Sampling
class MockSession:
    async def create_message(self, messages, max_tokens, system_prompt):
        # Mocking the result structure
        class MockContent:
            text = "Mock Advice: Stay cool!"
        class MockResult:
            content = MockContent()
        return MockResult()

class MockContext:
    session = MockSession()

async def main():
    print("Running verification with MOCK data...")
    
    # 1. Fetch (Skipped, using mocks)
    print("Fetch step skipped (using mocks).")
    geo, weather, aqi = MOCK_GEO, MOCK_WEATHER, MOCK_AQI

    # 2. Process
    try:
        processed = process_logic(geo, weather, aqi)
        print("Process successful!")
        print(processed)
    except Exception as e:
        print(f"Process failed: {e}")
        traceback.print_exc()
        return

    # 3. Advisor (Strategy Pattern)
    try:
        advisor = get_advisor()
        print(f"Advisor Strategy: {advisor.__class__.__name__}")
        # Only test SamplingStrategy if we have a context, or if API mode is set.
        # Assuming defaults (SAMPLING)
        advice = await advisor.generate_advice(processed, mcp_context=MockContext())
        print(f"Advice generated: {advice}")
        processed["advice_msg"] = advice
    except Exception as e:
        print(f"Advisor failed: {e}")
        traceback.print_exc()
        return

    # 4. Validate
    try:
        validated = validate_payload(processed)
        print("Validation successful!")
        print(validated)
    except Exception as e:
        print(f"Validation failed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
