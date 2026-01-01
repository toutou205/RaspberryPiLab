import httpx
import asyncio

async def main():
    print("Probing https://geocoding-api.open-meteo.com...")
    try:
        async with httpx.AsyncClient(verify=False) as client:
            resp = await client.get("https://geocoding-api.open-meteo.com/v1/search?name=London&count=1")
            print(f"Status: {resp.status_code}")
            print(resp.text[:100])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
