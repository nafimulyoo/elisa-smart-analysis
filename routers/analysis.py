# app/routers/analysis.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from datetime import datetime, timedelta
import json
from tools import async_fetch_compare, async_fetch_heatmap, async_fetch_monthly, async_fetch_daily, async_fetch_now
from mas_llm.actions.analyze_page import AnalyzePage


router = APIRouter(prefix="/api/analysis", tags=["analysis"])

@router.get("/faculty")
async def get_faculty_analysis(date: str):
    data = await async_fetch_compare(date)
    analyze_page = AnalyzePage()

    date_in_datetime = datetime.strptime(date, "%Y-%m")
    past_month_in_datetime = date_in_datetime.replace(day=1) - timedelta(days=1)

    past_month = past_month_in_datetime.strftime("%Y-%m")

    history = await async_fetch_compare(past_month)

    result = await analyze_page.run("compare_faculty", json.dumps(data), json.dumps(history))
    return result


@router.get("/heatmap")
async def get_monthly_analysis(start: str, end: str, faculty: str = None, building: str = None):
    data = await async_fetch_heatmap(start, end, faculty, building)
    analyze_page = AnalyzePage()

    start_date_in_datetime = datetime.strptime(start, "%Y-%m-%d")
    end_date_in_datetime = datetime.strptime(end, "%Y-%m-%d")

    past_week_start_in_datetime = start_date_in_datetime - timedelta(days=7)
    past_week_end_in_datetime = end_date_in_datetime - timedelta(days=7)

    past_week_start = past_week_start_in_datetime.strftime("%Y-%m-%d")
    past_week_end = past_week_end_in_datetime.strftime("%Y-%m-%d")

    history = await async_fetch_heatmap(past_week_start, past_week_end, faculty, building)
    
    result = await analyze_page.run("heatmap", json.dumps(data), json.dumps(history))
    return result

@router.get("/now")
async def get_now_analysis(date: str, faculty: str = "", building: str = "", floor: str = ""):
    data = await async_fetch_now(date, faculty, building, floor)
    analyze_page = AnalyzePage()
    date_in_datetime = datetime.strptime(date, "%Y-%m-%d")
    past_week_in_datetime = date_in_datetime - timedelta(days=7)

    history = await async_fetch_heatmap(past_week_in_datetime.strftime("%Y-%m-%d"), date, faculty, building)

    result = await analyze_page.run("now", json.dumps(data), json.dumps(history))
    return result

@router.get("/daily")
async def get_daily_analysis(date: str, faculty: str = "", building: str = "", floor: str = ""):
    data = await async_fetch_daily(date, faculty, building, floor)
    analyze_page = AnalyzePage()
    date_in_datetime = datetime.strptime(date, "%Y-%m-%d")
    past_week_in_datetime = date_in_datetime - timedelta(days=7)

    history = await async_fetch_heatmap(past_week_in_datetime.strftime("%Y-%m-%d"), date, faculty, building)

    result = await analyze_page.run("daily", json.dumps(data), json.dumps(history))
    return result

@router.get("/monthly")
async def get_monthly_analysis(date: str, faculty: str = "", building: str = "", floor: str = ""):
    data = await async_fetch_monthly(date, faculty, building, floor)
    analyze_page = AnalyzePage()
    history = []
    year_string = date.split("-")[0]
    month_string = date.split("-")[1]
    for i in range(0, 3):
        month = int(month_string) - i
        if month <= 0:
            month += 12
            year = int(year_string) - 1
        else:
            year = int(year_string)

        if month < 10:
            month_string = f"0{month}"
        else:
            month_string = str(month)

        history_data = await async_fetch_monthly(f"{year}-{month_string}", faculty, building, floor)
        history.append(history_data)

    result = await analyze_page.run("monthly", json.dumps(data), json.dumps({}))

    return result

