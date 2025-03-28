# app/routers/analysis.py
from fastapi import APIRouter, Depends, HTTPException, status
import asyncio
from typing import Annotated
from datetime import datetime, timedelta
import json
from tools import async_fetch_compare, async_fetch_heatmap, async_fetch_monthly, async_fetch_daily, async_fetch_now
from mas_llm.actions.analyze_page import now_analysis, heatmap_analysis, compare_faculty_analysis, daily_analysis, monthly_analysis


router = APIRouter(prefix="/api/analysis", tags=["analysis"])

@router.get("/now")
async def get_now_analysis(date: str, faculty: str = "", building: str = "", floor: str = ""):
    date_in_datetime = datetime.strptime(date, "%Y-%m-%d")
    past_week_in_datetime = date_in_datetime - timedelta(days=7)

    # Fetch data concurrently
    data_task = asyncio.create_task(async_fetch_now(date, faculty, building, floor))
    history_task = asyncio.create_task(async_fetch_heatmap(past_week_in_datetime.strftime("%Y-%m-%d"), date, faculty, building))

    data = await data_task
    history = await history_task

    result = await now_analysis(data, history)
    return result

@router.get("/daily")
async def get_daily_analysis(date: str, faculty: str = "", building: str = "", floor: str = ""):
    date_in_datetime = datetime.strptime(date, "%Y-%m-%d")
    past_week_in_datetime = date_in_datetime - timedelta(days=7)

    # Fetch data concurrently
    data_task = asyncio.create_task(async_fetch_daily(date, faculty, building, floor))
    history_task = asyncio.create_task(async_fetch_heatmap(past_week_in_datetime.strftime("%Y-%m-%d"), date, faculty, building))

    data = await data_task
    history = await history_task

    result = await daily_analysis(data, history)
    return result


@router.get("/monthly")
async def get_monthly_analysis(date: str, faculty: str = "", building: str = "", floor: str = ""):
    # Fetch main data
    data = await async_fetch_monthly(date, faculty, building, floor)
    
    # Prepare for historical data fetching
    year_string, month_string = date.split("-")

    data_task = asyncio.create_task(async_fetch_monthly(date, faculty, building, floor))
    history_task = [None] * 3  
    
    for i in range(3):
        month = int(month_string) - i
        year = int(year_string)
        
        if month <= 0:
            month += 12
            year -= 1
            
        month_string = f"0{month}" if month < 10 else str(month)
        
        history_task[i] = asyncio.create_task(async_fetch_monthly(f"{year}-{month_string}", faculty, building, floor))
    
    data = await data_task
    history = [None] * 3  

    for i in range(3):
        history[i] = await history_task[i]
        
    result = await monthly_analysis(data, history)

    return result


@router.get("/heatmap")
async def get_heatmap_analysis(start: str, end: str, faculty: str = None, building: str = None):

    start_date_in_datetime = datetime.strptime(start, "%Y-%m-%d")
    end_date_in_datetime = datetime.strptime(end, "%Y-%m-%d")

    past_week_start_in_datetime = start_date_in_datetime - timedelta(days=7)
    past_week_end_in_datetime = end_date_in_datetime - timedelta(days=7)

    past_week_start = past_week_start_in_datetime.strftime("%Y-%m-%d")
    past_week_end = past_week_end_in_datetime.strftime("%Y-%m-%d")
    
    # Fetch data concurrently
    data_task = asyncio.create_task(async_fetch_heatmap(start, end, faculty, building))
    history_task = asyncio.create_task(async_fetch_heatmap(past_week_start, past_week_end, faculty, building))
    
    data = await data_task
    history = await history_task

    result = await heatmap_analysis(data, history)
    return result


@router.get("/faculty")
async def get_faculty_analysis(date: str):
    
    date_in_datetime = datetime.strptime(date, "%Y-%m")
    past_month_in_datetime = date_in_datetime.replace(day=1) - timedelta(days=1)
    past_month = past_month_in_datetime.strftime("%Y-%m")

    # Fetch data concurrently
    data_task = asyncio.create_task(async_fetch_compare(date))
    history_task = asyncio.create_task(async_fetch_compare(past_month))

    data = await data_task
    history = await history_task

    result = await compare_faculty_analysis(data, history)
    return result




