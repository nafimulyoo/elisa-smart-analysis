# app/routers/analysis.py
from fastapi import APIRouter, Depends, HTTPException, status
import asyncio
from typing import Annotated
from datetime import datetime, timedelta
import json
from utils.elisa_api_cache import async_fetch_compare, async_fetch_heatmap, async_fetch_monthly, async_fetch_daily, async_fetch_now, async_fetch_fakultas, async_fetch_gedung, async_fetch_lantai
from mas_llm.actions.analyze_page import now_analysis, heatmap_analysis, compare_faculty_analysis, daily_analysis, monthly_analysis
from pyinstrument import Profiler
from functools import wraps
import time

def profile_endpoint(async_mode=True):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Initialize profiler (enable async mode)
            profiler = Profiler(async_mode=async_mode)
            profiler.start()

            # Execute the endpoint
            start_time = time.time()
            result = await func(*args, **kwargs)
            end_time = time.time()

            # Stop profiling and print results
            profiler.stop()
            print(f"\n=== Profiling results for {func.__name__} ===")
            print(f"Total time: {end_time - start_time:.2f}s")
            print(profiler.output_text(unicode=True, color=True))
            profiler.write_html("profile_report.html")

            return result
        return wrapper
    return decorator

data_router = APIRouter(prefix="/api", tags=["data"])

@data_router.get("/now")
@profile_endpoint()
async def get_now_analysis(faculty: str = "", building: str = "", floor: str = ""):
    return await async_fetch_now(faculty, building, floor)

@data_router.get("/daily")
@profile_endpoint()
async def get_daily_analysis(date: str, faculty: str = "", building: str = "", floor: str = ""):
    return await async_fetch_daily(date, faculty, building, floor)


@data_router.get("/monthly")
@profile_endpoint()
async def get_monthly_analysis(date: str, faculty: str = "", building: str = "", floor: str = ""):
    return await async_fetch_monthly(date, faculty, building, floor)


@data_router.get("/heatmap")
@profile_endpoint()
async def get_heatmap_analysis(start: str, end: str, faculty: str = None, building: str = None, floor: str = None):
    return await async_fetch_heatmap(start, end, faculty, building, floor)


@data_router.get("/compare")
@profile_endpoint()
async def get_compare(date: str):
    return await async_fetch_compare(date)

@data_router.get("/get-fakultas")
@profile_endpoint()
async def get_faculty():
    return await async_fetch_fakultas()

@data_router.get("/get-gedung")
@profile_endpoint()
async def get_building(fakultas: str):
    return await async_fetch_gedung(fakultas)

@data_router.get("/get-lantai")
@profile_endpoint()
async def get_floor(fakultas: str, gedung: str):
    return await async_fetch_lantai(fakultas, gedung)



