
import asyncio
from datetime import datetime, date, timedelta
from functools import wraps
import time
from typing import Optional, Tuple, Any
import re
import requests

# Cache setup
CACHE_CONFIG = {
    "now": {"size": 100, "ttl": 30},          # 30 seconds
    "daily": {"size": 100, "ttl": 900},       # 15 minutes
    "monthly": {"size": 100, "ttl": 7200},    # 2 hours
    "heatmap": {"size": 100, "ttl": 900},     # 15 minutes
    "compare": {"size": 100, "ttl": 7200},    # 2 hours
    "fakultas": {"size": 100, "ttl": float('inf')},  # Unlimited
    "gedung": {"size": 100, "ttl": float('inf')},    # Unlimited
}

# Cache storage
caches = {name: {} for name in CACHE_CONFIG}
cache_timestamps = {name: {} for name in CACHE_CONFIG}
cache_orders = {name: [] for name in CACHE_CONFIG}

def get_cache_key(func_name: str, *args, **kwargs) -> Tuple:
    """Generate a cache key based on function name and arguments"""
    if func_name == "fakultas":
        return ("fakultas",)  # Always same key since no arguments
    elif func_name == "gedung":
        return ("gedung", kwargs.get("fakultas", ""))
    return tuple(args) + (frozenset(kwargs.items()),)

def parse_date(date_str: str) -> Optional[date]:
    """Parse different date formats used in the API"""
    if not date_str:
        return None
    
    try:
        if re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):  # YYYY-MM-DD
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        elif re.match(r"^\d{4}-\d{2}$", date_str):  # YYYY-MM
            return datetime.strptime(date_str, "%Y-%m").date()
    except ValueError:
        pass
    return None

def cached(func_name: str):
    """Decorator factory for caching with specific TTL"""
    config = CACHE_CONFIG[func_name]
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = get_cache_key(func_name, *args, **kwargs)
            
            # Check cache
            if cache_key in caches[func_name]:
                cached_time = cache_timestamps[func_name][cache_key]
                if time.time() - cached_time < config["ttl"]:
                    # Move to end of order (most recently used)
                    if cache_key in cache_orders[func_name]:
                        cache_orders[func_name].remove(cache_key)
                    cache_orders[func_name].append(cache_key)
                    return caches[func_name][cache_key]
            
            # Not in cache or expired - fetch fresh
            result = await func(*args, **kwargs)
            
            # Add to cache
            caches[func_name][cache_key] = result
            cache_timestamps[func_name][cache_key] = time.time()
            cache_orders[func_name].append(cache_key)
            
            # Enforce cache size
            if len(caches[func_name]) > config["size"]:
                oldest_key = cache_orders[func_name].pop(0)
                del caches[func_name][oldest_key]
                del cache_timestamps[func_name][oldest_key]
            
            return result
        return wrapper
    return decorator

async def fetch_with_retry(url: str, max_retries: int = 3):
    """Helper function to fetch with retries"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, verify=False)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            await asyncio.sleep(1 * (attempt + 1))

# API functions with appropriate caching

@cached("now")
async def async_fetch_now(faculty: str = "", building: str = "", floor: str = ""):
    """Fetch real-time energy data with 30-second cache"""
    url = f"https://elisa.itb.ac.id/api/now?faculty={faculty}&building={building}&floor={floor}"
    return await fetch_with_retry(url)

@cached("daily")
async def async_fetch_daily(date: str, faculty: str = "", building: str = "", floor: str = ""):
    """Fetch daily data with 15-minute cache"""
    url = f"https://elisa.itb.ac.id/api/daily?date={date}&faculty={faculty}&building={building}&floor={floor}"
    return await fetch_with_retry(url)

@cached("monthly")
async def async_fetch_monthly(date: str, faculty: str = "", building: str = "", floor: str = ""):
    """Fetch monthly data with 2-hour cache"""
    url = f"https://elisa.itb.ac.id/api/monthly?date={date}&faculty={faculty}&building={building}&floor={floor}"
    return await fetch_with_retry(url)

@cached("heatmap")
async def async_fetch_heatmap(start: str, end: str, faculty: str = "", building: str = "", floor: str = ""):
    """Fetch heatmap data with 15-minute cache"""
    url = f"https://elisa.itb.ac.id/api/heatmap?faculty={faculty}&start={start}&end={end}&building={building}&floor={floor}"
    return await fetch_with_retry(url)

@cached("compare")
async def async_fetch_compare(date: str):
    """Fetch comparison data with 2-hour cache"""
    url = f"https://elisa.itb.ac.id/api/compare?date={date}"
    return await fetch_with_retry(url)

@cached("fakultas")
async def async_fetch_fakultas():
    """Fetch faculties list with unlimited cache"""
    url = "https://elisa.itb.ac.id/api/get-fakultas"
    return await fetch_with_retry(url)

@cached("gedung")
async def async_fetch_gedung(fakultas: str):
    """Fetch buildings list with unlimited cache"""
    url = f"https://elisa.itb.ac.id/api/get-gedung?fakultas={fakultas}"
    return await fetch_with_retry(url)

async def async_fetch_lantai(fakultas: str, gedung: str):
    """Fetch floors list with no caching"""
    url = f"https://elisa.itb.ac.id/api/get-lantai?fakultas={fakultas}&gedung={gedung}"
    return await fetch_with_retry(url)