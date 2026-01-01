from abc import ABC, abstractmethod
import httpx
from mcp.server.fastmcp import Context
from mcp.types import TextContent, SamplingMessage, Role
from config import Config

# 建议策略类：实现 Strategy Pattern (Sampling vs Direct API)

class AdviceStrategy(ABC):
    @abstractmethod
    async def generate_advice(self, context_data: dict, mcp_context: Context = None) -> str:
        """
        Generates advice string.
        mcp_context is required for Sampling strategy.
        """
        pass

class SamplingStrategy(AdviceStrategy):
    async def generate_advice(self, context_data: dict, mcp_context: Context = None) -> str:
        if not mcp_context:
            return "Sampling Context Missing."

        prompt = self._build_prompt(context_data)
        
        try:
            # Call MCP Sampling
            # Construct message using SamplingMessage
            message = SamplingMessage(
                role="user",
                content=TextContent(type="text", text=prompt)
            )
            
            result = await mcp_context.session.create_message(
                messages=[message],
                max_tokens=50, # Short advice
                system_prompt="You are a witty health consultant. Keep advice under 32 chars."
            )
            
            # Extract text from result
            # result is CreateMessageResult
            if result.content and hasattr(result.content, 'text'):
                 advice = result.content.text
            elif hasattr(result, 'content') and isinstance(result.content, TextContent):
                 advice = result.content.text
            elif isinstance(result, TextContent):
                 # Some versions return content directly
                 advice = result.text
            else:
                 # Fallback
                 advice = str(result)

            return self._truncate(advice)
            return self._truncate(advice)
        except Exception as e:
            import sys, traceback
            traceback.print_exc(file=sys.stderr)
            return f"Advice Error: {type(e).__name__}: {str(e)}"

    def _build_prompt(self, data: dict) -> str:
        return (
            f"Generate specific health advice (Max 32 chars) based on WHO standards.\n"
            f"Data: Temp={data['temperature']}C, AQI={data['aqi']}, Weather={data['weather_desc']}.\n"
            f"Examples:\n"
            f"- 'Perfect day! Open windows.'\n"
            f"- 'Toxic air! Stay home.'\n"
            f"Output only the advice string."
        )

    def _truncate(self, text: str) -> str:
        cleaned = text.strip().replace('"', '').replace('\n', ' ')
        if len(cleaned) <= 32:
            return cleaned
        
        truncated = cleaned[:32]
        last_space = truncated.rfind(' ')
        if last_space > 0:
            return truncated[:last_space]
        return truncated

class DirectApiStrategy(AdviceStrategy):
    async def generate_advice(self, context_data: dict, mcp_context: Context = None) -> str:
        api_key = Config.GEMINI_API_KEY
        if not api_key:
            return "API Key Missing."

        prompt = self._build_prompt(context_data)
        
        # Call Gemini API via httpx
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, json=payload, timeout=5.0)
                if resp.status_code != 200:
                    return "API Error."
                
                data = resp.json()
                # Parse Gemini response
                try:
                    text = data['candidates'][0]['content']['parts'][0]['text']
                    return self._truncate(text)
                except (KeyError, IndexError):
                    return "Parse Error."
        except Exception:
            return "Net Error."

    def _build_prompt(self, data: dict) -> str:
        # Tighter constraint for safety
        return (
            f"You are a witty health consultant. Generate advice under 25 chars based on WHO standards.\n"
            f"Data: Temp={data['temperature']}C, AQI={data['aqi']}, Weather={data['weather_desc']}.\n"
            f"Output only the advice text."
        )

    def _truncate(self, text: str) -> str:
        cleaned = text.strip().replace('"', '').replace('\n', ' ')
        if len(cleaned) <= 32:
            return cleaned
        
        # Hard truncate to 32 first
        truncated = cleaned[:32]
        # Try to cut at the last space to avoid split words
        last_space = truncated.rfind(' ')
        if last_space > 0:
            return truncated[:last_space]
        return truncated

def get_advisor() -> AdviceStrategy:
    mode = Config.ADVICE_MODE
    if mode == "API":
        return DirectApiStrategy()
    return SamplingStrategy()
