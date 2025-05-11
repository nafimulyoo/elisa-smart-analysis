import asyncio
from datetime import datetime, date
from functools import wraps
import time
from typing import Optional, Tuple, Any, Dict, List
import re
import aiohttp
from async_lru import alru_cache
import json

# Constants
DATE_FORMATS = (
    (r"^\d{4}-\d{2}-\d{2}$", "%Y-%m-%d"),  # YYYY-MM-DD
    (r"^\d{4}-\d{2}$", "%Y-%m")            # YYYY-MM
)

# Cache configuration
CACHE_CONFIG = {
    "now": {"size": 100, "ttl": 15},          # 30 seconds
    "daily": {"size": 100, "ttl": 900},       # 15 minutes
    "monthly": {"size": 100, "ttl": 7200},    # 2 hours
    "heatmap": {"size": 100, "ttl": 900},     # 15 minutes
    "compare": {"size": 100, "ttl": 7200},    # 2 hours
    "fakultas": {"size": 100, "ttl": None},   # Unlimited (None means no TTL)
    "gedung": {"size": 100, "ttl": None},     # Unlimited
}

# Pre-compiled regex patterns
DATE_PATTERNS = [re.compile(pattern) for pattern, _ in DATE_FORMATS]

# Global session for connection pooling
SESSION = None

async def get_session():
    """Get or create aiohttp session with connection pooling"""
    global SESSION
    if SESSION is None or SESSION.closed:
        connector = aiohttp.TCPConnector(
            limit=100,
            force_close=False,
            enable_cleanup_closed=True,
            ssl=False
        )
        timeout = aiohttp.ClientTimeout(total=30)
        SESSION = aiohttp.ClientSession(connector=connector, timeout=timeout)
    return SESSION

def parse_date(date_str: str) -> Optional[date]:
    """Optimized date parsing with pre-compiled patterns"""
    if not date_str:
        return None
    
    for pattern, date_format in zip(DATE_PATTERNS, DATE_FORMATS):
        if pattern.match(date_str):
            try:
                return datetime.strptime(date_str, date_format[1]).date()
            except ValueError:
                continue
    return None

def get_cache_key(func_name: str, *args, **kwargs) -> Tuple:
    """Optimized cache key generation"""
    if func_name == "fakultas":
        return ("fakultas",)
    if func_name == "gedung":
        return ("gedung", kwargs.get("fakultas", ""))
    return args + (frozenset(kwargs.items()),)

def cached(func_name: str):
    """Optimized caching decorator with LRU and TTL"""
    config = CACHE_CONFIG[func_name]
    
    # Special case for unlimited TTL - use async_lru
    if config["ttl"] is None:
        def decorator(func):
            cached_func = alru_cache(maxsize=config["size"])(func)
            @wraps(func)
            async def wrapper(*args, **kwargs):
                return await cached_func(*args, **kwargs)
            return wrapper
        return decorator
    
    # For TTL-based caching
    def decorator(func):
        cache = {}
        timestamps = {}
        keys_order = []
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            nonlocal cache, timestamps, keys_order
            cache_key = get_cache_key(func_name, *args, **kwargs)
            now = time.monotonic()
            
            # Cache hit
            if cache_key in cache:
                if now - timestamps[cache_key] < config["ttl"]:
                    # Update access time and move to end
                    timestamps[cache_key] = now
                    keys_order.remove(cache_key)
                    keys_order.append(cache_key)
                    return cache[cache_key]
                # Expired - remove
                del cache[cache_key]
                del timestamps[cache_key]
                keys_order.remove(cache_key)
            
            # Cache miss - fetch fresh data
            result = await func(*args, **kwargs)
            
            # Add to cache
            cache[cache_key] = result
            timestamps[cache_key] = now
            keys_order.append(cache_key)
            
            # Enforce size limit
            if len(cache) > config["size"]:
                oldest_key = keys_order.pop(0)
                del cache[oldest_key]
                del timestamps[oldest_key]
            
            return result
        
        return wrapper
    return decorator

async def fetch_with_retry(url: str, max_retries: int = 3, timeout: float = 5.0):
    """Optimized fetch with retries using aiohttp"""
    session = await get_session()
    
    for attempt in range(max_retries):
        try:
            async with session.get(url, ssl=False) as response:
                if response.status == 200:
                    text_response = await response.text()
                    return json.loads(text_response)
                elif response.status >= 500:
                    await asyncio.sleep(1 * (attempt + 1))
                    continue
                response.raise_for_status()
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            if attempt == max_retries - 1:
                raise e
            await asyncio.sleep(1 * (attempt + 1))
    
    raise aiohttp.ClientError(f"Failed after {max_retries} retries")

# API functions with optimized caching

#@cached("now")
async def async_fetch_now(faculty: str = "", building: str = "", floor: str = ""):
    """Fetch real-time energy data with 30-second cache"""
    url = f"https://elisa.itb.ac.id/api/now?faculty={faculty}&building={building}&floor={floor}"
    return await fetch_with_retry(url)

#@cached("daily")
async def async_fetch_daily(date: str, faculty: str = "", building: str = "", floor: str = ""):
    """Fetch daily data with 15-minute cache"""
    url = f"https://elisa.itb.ac.id/api/daily?date={date}&faculty={faculty}&building={building}&floor={floor}"
    print(f"Fetching daily data from {url}")
    return await fetch_with_retry(url)

#@cached("monthly")
async def async_fetch_monthly(date: str, faculty: str = "", building: str = "", floor: str = ""):
    """Fetch monthly data with 2-hour cache"""
    url = f"https://elisa.itb.ac.id/api/monthly?date={date}&faculty={faculty}&building={building}&floor={floor}"
    print(f"Fetching monthly data from {url}")
    return await fetch_with_retry(url)

#@cached("heatmap")
async def async_fetch_heatmap(start: str, end: str, faculty: str = "", building: str = "", floor: str = ""):
    """Fetch heatmap data with 15-minute cache"""
    url = f"https://elisa.itb.ac.id/api/heatmap?faculty={faculty}&start={start}&end={end}&building={building}&floor={floor}"
    return await fetch_with_retry(url)

#@cached("compare")
async def async_fetch_compare(date: str):
    """Fetch comparison data with 2-hour cache"""
    url = f"https://elisa.itb.ac.id/api/compare?date={date}"
    return await fetch_with_retry(url)

#@cached("fakultas")
async def async_fetch_fakultas():
    """Fetch faculties list with unlimited cache"""
    url = "https://elisa.itb.ac.id/api/get-fakultas"
    return await fetch_with_retry(url)

#@cached("gedung")
async def async_fetch_gedung(fakultas: str):
    """Fetch buildings list with unlimited cache"""
    url = f"https://elisa.itb.ac.id/api/get-gedung?fakultas={fakultas}"
    return await fetch_with_retry(url)

async def async_fetch_lantai(fakultas: str, gedung: str):
    """Fetch floors list with no caching"""
    url = f"https://elisa.itb.ac.id/api/get-lantai?fakultas={fakultas}&gedung={gedung}"
    return await fetch_with_retry(url)

async def close_session():
    """Cleanup session when done"""
    global SESSION
    if SESSION and not SESSION.closed:
        await SESSION.close()