import httpx
from config import Config

# 封装 AQICN 的异步请求逻辑

class AQICNClient:
    BASE_URL = "https://api.waqi.info/feed"

    def __init__(self):
        self.token = Config.AQICN_API_KEY
        if not self.token:
             # In a real app we might fallback or warn, but for now we proceed.
             pass

    async def get_air_quality(self, lat: float, lon: float):
        """
        Get air quality data for the given coordinates.
        """
        if not self.token:
            return {"aqi": 0, "pm25": 0.0} # Fail safe
        
        url = f"{self.BASE_URL}/geo:{lat};{lon}/"
        # httpx automatically reads HTTPS_PROXY and HTTP_PROXY from environment
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params={"token": self.token}, timeout=10.0)
            resp.raise_for_status()
            data = resp.json()
            
            if data["status"] != "ok":
                # Handle error or return default
                return {"aqi": 0, "pm25": 0.0}
            
            result = data.get("data", {})
            aqi = result.get("aqi", 0)
            if aqi == '-': # Sometimes API returns '-'
                aqi = 0
            
            iaqi = result.get("iaqi", {})
            pm25 = iaqi.get("pm25", {}).get("v", 0.0)
            
            return {
                "aqi": int(aqi),
                "pm25": float(pm25)
            }
