# app/routers/analysis.py
from fastapi import APIRouter, HTTPException
import asyncio
from datetime import datetime, timedelta
from utils.elisa_api_cache import async_fetch_compare, async_fetch_heatmap, async_fetch_monthly, async_fetch_daily, async_fetch_now
from mas_llm.actions.analyze_page import now_analysis, heatmap_analysis, compare_faculty_analysis, daily_analysis, monthly_analysis
import aiohttp


analysis_router = APIRouter(prefix="/api/analysis", tags=["analysis"])

async def handle_elisa_response(data_task, analysis_func, *args, **kwargs):
    try:
        # raise aiohttp.ClientError("Simulated error")  # Simulate an error for testing
        data = await data_task
        analysis = await analysis_func(data, *args, **kwargs)
        # testing
        return {"analysis": analysis}
    except aiohttp.ClientError as e:
        # First check if it's a connection-level error
        if isinstance(e, (aiohttp.ClientConnectorError, aiohttp.ServerTimeoutError)):
            return {
                "analysis": "There is a problem in communication between client and ELISA. The ELISA service appears to be down.",
                "error": str(e)
            }
        # If we got a response but it failed (4xx/5xx)
        return {
            "analysis": "There appears to be a problem with the data or sensors. While ELISA is reachable, the data could not be properly retrieved or processed.",
            "error": str(e)
        }

@analysis_router.get("/now")
async def get_now_analysis(faculty: str = "", building: str = "", floor: str = "", model: str = ""):
    data_task = asyncio.create_task(async_fetch_now(faculty, building, floor))
    return await handle_elisa_response(
        data_task, 
        now_analysis, 
        faculty=faculty, 
        building=building, 
        floor=floor,
        model=model
    )

@analysis_router.get("/daily")
async def get_daily_analysis(date: str, faculty: str = "", building: str = "", floor: str = "", model: str = ""):
    data_task = asyncio.create_task(async_fetch_daily(date, faculty, building, floor))
    return await handle_elisa_response(
        data_task,
        daily_analysis,
        date,
        faculty=faculty,
        building=building,
        floor=floor,
        model=model
    )

@analysis_router.get("/monthly")
async def get_monthly_analysis(date: str, faculty: str = "", building: str = "", floor: str = "", model: str = ""):
    data_task = asyncio.create_task(async_fetch_monthly(date, faculty, building, floor))
    return await handle_elisa_response(
        data_task,
        monthly_analysis,
        date,
        faculty=faculty,
        building=building,
        floor=floor,
        model=model
    )

@analysis_router.get("/faculty")
async def get_faculty_analysis(date: str, model: str = ""):
    date_in_datetime = datetime.strptime(date, "%Y-%m")
    past_month_in_datetime = date_in_datetime.replace(day=1) - timedelta(days=1)
    past_month = past_month_in_datetime.strftime("%Y-%m")

    # Create tasks for both current and historical data
    data_task = asyncio.create_task(async_fetch_compare(date))
    history_task = asyncio.create_task(async_fetch_compare(past_month))

    # Use a wrapper function to handle both data fetches
    async def faculty_data_handler():
        data, history = await asyncio.gather(data_task, history_task)
        return {"data": data, "history": history}

    # Process through the unified handler
    result = await handle_elisa_response(
        faculty_data_handler(),
        lambda x: compare_faculty_analysis(x["data"], x["history"], date, model=model)
    )
    
    # If we got an error response, return it directly
    if "error" in result:
        return result
    
    return {"analysis": result["analysis"]}


@analysis_router.get("/heatmap")
async def get_heatmap_analysis(start: str, end: str, faculty: str = None, building: str = None, floor: str = None, model: str = ""):
    start_date_in_datetime = datetime.strptime(start, "%Y-%m-%d")
    end_date_in_datetime = datetime.strptime(end, "%Y-%m-%d")

    past_week_start_in_datetime = start_date_in_datetime - timedelta(days=7)
    past_week_end_in_datetime = end_date_in_datetime - timedelta(days=7)

    past_week_start = past_week_start_in_datetime.strftime("%Y-%m-%d")
    past_week_end = past_week_end_in_datetime.strftime("%Y-%m-%d")
    
    # Create tasks for both current and historical data
    data_task = asyncio.create_task(async_fetch_heatmap(start, end, faculty, building, floor))
    history_task = asyncio.create_task(async_fetch_heatmap(past_week_start, past_week_end, faculty, building, floor))

    # Use a wrapper function to handle both data fetches
    async def heatmap_data_handler():
        data, history = await asyncio.gather(data_task, history_task)
        return {"data": data, "history": history}

    # Process through the unified handler
    result = await handle_elisa_response(
        heatmap_data_handler(),
        lambda x: heatmap_analysis(x["data"], x["history"], faculty=faculty, building=building, floor=floor, model=model)
    )
    
    # If we got an error response, return it directly
    if "error" in result:
        return result
    
    return {"analysis": result["analysis"]}


# def profile_endpoint(async_mode=True):
#     def decorator(func):
#         @wraps(func)
#         async def wrapper(*args, **kwargs):
#             # Initialize profiler (enable async mode)
#             profiler = Profiler(async_mode=async_mode)
#             profiler.start()

#             # Execute the endpoint
#             start_time = time.time()
#             result = await func(*args, **kwargs)
#             end_time = time.time()

#             # Stop profiling and print results
#             profiler.stop()
#             print(f"\n=== Profiling results for {func.__name__} ===")
#             print(f"Total time: {end_time - start_time:.2f}s")
#             print(profiler.output_text(unicode=True, color=True))
#             profiler.write_html("profile_report.html")

#             return result
#         return wrapper
#     return decorator


