from datetime import datetime, timedelta
try:
    from zoneinfo import ZoneInfo
except ImportError:
    # Fallback for Python < 3.9
    try:
        import pytz
        ZoneInfo = None
    except ImportError:
        pytz = None
        ZoneInfo = None

# 处理时区与格式化时间字符串

def get_local_time(timezone_str: str = "", utc_offset_seconds: int = 0) -> datetime:
    """
    Calculates the local time based on timezone string or UTC offset.
    """
    now_utc = datetime.utcnow()
    
    if timezone_str:
        try:
            if ZoneInfo:
                tz = ZoneInfo(timezone_str)
                return datetime.now(tz)
            elif pytz:
                tz = pytz.timezone(timezone_str)
                now_utc = pytz.UTC.localize(now_utc)
                return now_utc.astimezone(tz)
        except Exception:
            pass # Fallback to offset
            
    # Use UTC offset
    tz_offset = timedelta(seconds=utc_offset_seconds)
    return now_utc + tz_offset

def format_timestamp(dt: datetime) -> str:
    """
    Formats the timestamp as 'YY/MM/DD HH:mm Week' (e.g., '23/12/31 15:30 Tue').
    """
    weekday_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return f"{dt.strftime('%y/%m/%d %H:%M')} {weekday_names[dt.weekday()]}"
