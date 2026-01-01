
import asyncio
from main import update_remote_display
# main.py usually defines the tool but doesnt run `mcp.run()` if imported?
# Actually main.py has `if __name__ == "__main__": mcp.run()`.
# We can import the function `update_remote_display` directly.
# However, `update_remote_display` uses `ctx`. In verification we might need to mock Context or use FastMCP's test capabilities.
# Wait, FastMCP is an object. `update_remote_display` is decorated.
# Let's inspect `verify_remote_display.py` content first. But creating a simple runner is faster.

# Actually, to simulate a real call without running the full server, we can just call it if we mock the context?
# Or we can just invoke the logic inside `main.py` if we extract it?
# No, `update_remote_display` is an async function.
# Let's write a script that invokes the underlying logic directly or mocks the context.

from mcp.server.fastmcp import Context

class MockContext(Context):
    def __init__(self):
        pass
    async def report_progress(self, progress: float, total: float | None = None):
        print(f"[Progress] {progress}/{total}")

    async def log(self, level, message):
        print(f"[Log-{level}] {message}")
        
    @property
    def request_id(self):
        return "test-req-id"
        
    @property
    def session(self):
        return None

async def test_deployment():
    cities = ["Shanghai", "Sydney", "London"]
    ctx = MockContext()
    
    print("=== Starting Deployment Verification ===")
    
    for city in cities:
        print(f"\n>> Testing City: {city}")
        try:
            # We import the decorated function. FastMCP wrapper usually allows direct call?
            # Let's try.
            result = await update_remote_display(city, ctx)
            print(f"Result for {city}: {result}")
        except Exception as e:
            print(f"FAILED for {city}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_deployment())
