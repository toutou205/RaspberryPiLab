"""Simple local client to test the MCP server."""
import asyncio
import os

from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession


def _build_server_params() -> StdioServerParameters:
    """Build StdioServerParameters so that `src` can be imported correctly."""
    return StdioServerParameters(
        command="ssh",
        args=[
            "-T",
            "alex@192.168.3.13",
            "bash -c 'PYTHONPATH=/home/alex/ProjectVenv/MCP_Sever_Practice/project_root_mcp /home/alex/ProjectVenv/bin/python -u /home/alex/ProjectVenv/MCP_Sever_Practice/project_root_mcp/src/main.py'"
        ],
        env=None,
    )


async def run() -> None:
    """Run a single test call against the MCP server."""
    server_params = _build_server_params()

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 模拟发送给屏幕的数据
            print("Sending data to display...")
            result = await session.call_tool(
                "display_weather_info",
                arguments={
                    "country_code": "CHN",
                    "city_name": "Beijing",
                    "timestamp": "25/12/30 14:00 Mon",
                    "weather_code": 100,  # 晴天 (mapped to icon 100.png)
                    "weather_desc": "Sunny",
                    "temperature": 2.5,
                    "aqi": 80,
                    "pm25": 35.0,
                    "warning_msg": "Good air quality today!",
                },
            )
            print("Tool result:", result)


if __name__ == "__main__":
    asyncio.run(run())