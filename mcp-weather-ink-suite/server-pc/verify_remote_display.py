
import asyncio
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
    city = "Zhuhai" # New city for testing
    print(f"Testing update_remote_display for {city}...")
    
    # We call the tool function directly.
    # Note: FastMCP tools are decorated functions, but the decoration might wrap them.
    # FastMCP decorators usually return the original function with metadata attached, 
    # or a callable wrapper. Let's try calling it.
    
    ctx = MockContext()
    result = await update_remote_display(city, ctx)
    print("Optimization Result:", result)

if __name__ == "__main__":
    asyncio.run(main())
