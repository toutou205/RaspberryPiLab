
import httpx
from config import Config

class CityNameNormalizer:
    @staticmethod
    async def normalize(raw_input: str) -> str:
        """
        Uses LLM to normalize diverse city inputs (Chinese, typos, specific formatting)
        into a standard English city name optimized for OpenMeteo search.
        
        Examples:
        "大理" -> "Dali"
        "Dali, Yunnan" -> "Dali"
        "Chaoyang, Beijing" -> "Beijing" (or specific district if supported)
        "The capital of Japan" -> "Tokyo"
        """
        api_key = Config.GEMINI_API_KEY
        if not api_key:
            return raw_input # Fallback to raw if no key

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        
        prompt = (
            f"Convert the location '{raw_input}' into a single, standard English city name "
            f"best suited for a weather API search (OpenMeteo). "
            f"If it's a district, prefer the main city unless the district is famous. "
            f"Return ONLY the English name, nothing else. No punctuation."
        )

        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        try:
            # httpx reads HTTPS_PROXY automatically
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, json=payload, timeout=5.0)
                if resp.status_code != 200:
                    return raw_input
                
                data = resp.json()
                try:
                    candidates = data.get('candidates', [])
                    if not candidates:
                        return raw_input
                    
                    text = candidates[0]['content']['parts'][0]['text']
                    normalized = text.strip().replace('\n', '').replace('.', '')
                    return normalized
                except (KeyError, IndexError):
                    return raw_input
        except Exception:
            return raw_input # Fail silently to raw input
