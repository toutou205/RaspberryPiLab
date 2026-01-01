import asyncio
import traceback
import os
# Set proxy if not already set
if not os.getenv("HTTPS_PROXY"):
    os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"
from main import update_remote_display
from mcp.server.fastmcp import Context

# Mock Context
class MockContext(Context):
    def __init__(self):
        pass
    def info(self, msg):
        print(f"INFO: {msg}")
    def error(self, msg):
        print(f"ERROR: {msg}")

async def main():
    city = "大理"  # Dali in Chinese
    print(f"Testing update_remote_display for {city}...")
    
    try:
        ctx = MockContext()
        result = await update_remote_display(city, ctx)
        print("Result:", result)
    except Exception as e:
        print(f"Exception caught: {type(e).__name__}")
        print(f"Exception message: {str(e)}")
        print(f"Exception args: {e.args}")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())

