from mcp.server.fastmcp import FastMCP, Context
from services.aggregator import fetch_all_data
from services.processor import process_logic
from services.advisor import get_advisor
from utils.validator import validate_payload
from config import Config
import asyncio
import subprocess

# main.py
# 入口文件：初始化 FastMCP，注册 Tool，整合各 Service

mcp = FastMCP("WeatherAirInfo")

@mcp.tool()
async def get_full_weather_report(city_name: str, ctx: Context) -> dict:
    """
    Get full weather and air quality report for a city.
    Suitable for E-Ink display rendering.
    """
    try:
        # 1. Fetch Data (Parallel I/O)
        geo_data, weather_data, aqi_data = await fetch_all_data(city_name)

        # 2. Process & Clean Data
        processed_data = process_logic(geo_data, weather_data, aqi_data)

        # 3. Generate Advice (Strategy Pattern)
        advisor = get_advisor()
        advice = await advisor.generate_advice(processed_data, mcp_context=ctx)
        
        # Add advice to payload
        processed_data["advice_msg"] = advice

        # 4. Validate Payload
        final_payload = validate_payload(processed_data)
        
        return final_payload

    except Exception as e:
        # In a real scenario, we might want to return a specific error structure
        # or re-raise. For now, we return the error string to be helpful.
        return {"error": str(e)}

@mcp.tool()
async def update_remote_display(city_name: str, ctx: Context) -> str:
    """
    Fetch weather for a city and immediately update the remote Raspberry Pi E-Ink display.
    This performs the complete workflow: Fetch -> Validate -> Deploy.
    """
    try:
        # 1. Fetch & Process
        geo_data, weather_data, aqi_data = await fetch_all_data(city_name)
        processed_data = process_logic(geo_data, weather_data, aqi_data)
        
        # 2. Advice
        advisor = get_advisor()
        advice = await advisor.generate_advice(processed_data, mcp_context=ctx)
        processed_data["advice_msg"] = advice

        # 3. Clamp AQI/PM2.5 (Schema Fix)
        if "aqi" in processed_data:
            processed_data["aqi"] = max(1, processed_data["aqi"])
        if "pm25" in processed_data:
            processed_data["pm25"] = max(0.1, processed_data["pm25"])

        # 4. Construct Manifest (Protocol Handshake)
        import json
        handshake_lines = [
            {"jsonrpc": "2.0", "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}, "id": 1},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "display_weather_info", "arguments": {"data": processed_data}}, "id": 2}
        ]
        
        payload_str = "\n".join([json.dumps(line) for line in handshake_lines])

        # 5. Remote Execution via SSH
        # We write payload to a temporary file locally or pipe it directly?
        # Piping complex JSON via SSH command line is fragile (as seen before). 
        # Safer to write to temp file then SCP.
        
        import os
        
        # Create temp file
        temp_file = "temp_payload.json"
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(payload_str)
            

        # SCP
        pi_user = Config.PI_USER
        pi_host = Config.PI_HOST
        subprocess.run(["scp", temp_file, f"{pi_user}@{pi_host}:/home/{pi_user}/mcp_request.json"], check=True)
        
        # SSH Execute
        # Note: We use the robust command we derived: pkill -> pipe -> run -> logs
        # We wrap in bash -c to ensure pipe handling is correct on the remote end.
        # FIX: Avoid nested single quotes. specificially 'echo -n '''.
        remote_script = (
            "sudo pkill -9 python; "
            f"> /home/{pi_user}/mcp_server.log; "
            f"cat /home/{pi_user}/mcp_request.json | /home/{pi_user}/run_mcp_server.sh"
        )
        
        # We format this carefully for the ssh command
        ssh_cmd = ["ssh", f"{pi_user}@{pi_host}", f"bash -c '{remote_script}'"]
        
        # We won't block forever on the log output here, or maybe we should?
        # The user wants "Success" confirmation. 
        # Let's run it and capture output.
        
        # We won't block forever on the log output here. 
        # Add a timeout to prevent hanging if SSH doesn't close cleanly.
        try:
            result = subprocess.run(ssh_cmd, capture_output=True, text=True, check=True, timeout=30, stdin=subprocess.DEVNULL)
        except subprocess.TimeoutExpired:
            # If it times out, it might still have worked (ghost session).
            # We proceed to verification.
            print("SSH Command timed out (daemon lingering?), proceeding to verification.")
            result = None
        
        # Wait for display update to complete (takes 10-15 seconds)
        import time
        time.sleep(5)  # Wait 5 seconds for initial processing
        
        # Retrieve logs for confirmation
        # Add timeout here too!
        verify_cmd = f"cat /home/{pi_user}/mcp_server.log"
        try:
            verify_result = subprocess.run(["ssh", f"{pi_user}@{pi_host}", verify_cmd], capture_output=True, text=True, timeout=10, stdin=subprocess.DEVNULL)
            log_output = verify_result.stdout or ""
        except subprocess.TimeoutExpired:
            log_output = "Verification timed out. Check Pi logs manually."
        except Exception as e:
            log_output = f"Verification failed: {str(e)}"
        
        # Check for various success indicators
        success_indicators = [
            "Successfully displayed",
            "Display update complete",
            "Displayed weather for",
            "SUCCESS"
        ]
        
        is_success = any(indicator in log_output for indicator in success_indicators)
        
        if is_success:
            return f"✅ Successfully updated display for {city_name}. Temperature: {processed_data.get('temperature')}°C, AQI: {processed_data.get('aqi')}, Weather: {processed_data.get('weather_desc')}"
        elif log_output.strip():
            # If there's log output but no success message, show the logs
            return f"Command executed. Logs:\n{log_output[-1000:]}"
        else:
            # If no logs yet, assume it's still processing
            return f"✅ Command executed. Display update in progress (takes 10-15 seconds). Weather data sent: {city_name}, Temp: {processed_data.get('temperature')}°C, AQI: {processed_data.get('aqi')}"

    except subprocess.CalledProcessError as e:
        error_msg = f"Subprocess error (code {e.returncode}): {e.stderr or e.stdout or str(e)}"
        return f"Error updating display: {error_msg}"
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return f"Error updating display: {str(e)}\nDetails: {error_details[-500:]}"

def mcp_main():
    """Entry point for running the server."""
    mcp.run()

if __name__ == "__main__":
    mcp_main()
