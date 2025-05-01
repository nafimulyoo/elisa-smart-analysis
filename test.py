from fastapi import APIRouter, HTTPException
import asyncio
from datetime import datetime, timedelta
from utils.elisa_api_cache import async_fetch_compare, async_fetch_heatmap, async_fetch_monthly, async_fetch_daily, async_fetch_now
from mas_llm.actions.analyze_page import now_analysis, heatmap_analysis, compare_faculty_analysis, daily_analysis, monthly_analysis
import aiohttp

async def check_elisa_availability():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("google.com", timeout=5, ssl=False) as response:
                return response.status == 200
    except:

        return False
    
print("Checking ELISA availability...")
avaoilable = asyncio.run(check_elisa_availability())
print(f"ELISA available: {avaoilable}")