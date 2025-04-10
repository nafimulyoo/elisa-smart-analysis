from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
print(sys.path)
# In your FastAPI app
import psutil
import os

from routers.ask import ask_router
from routers.analysis import analysis_router
from routers.health import health_router
from routers.data import data_router

from config import settings

app = FastAPI()


def kill_fastapi_processes():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'fastapi' in ' '.join(proc.info['cmdline'] or []):
            proc.kill()

@app.middleware("http")
async def restart_on_memory_limit(request, call_next):
    os.system("pkill -f ipykernel_launcher")
    if psutil.virtual_memory().percent > 80: 
        kill_fastapi_processes()
        os.system("fast run index.py")
        return {"message": "Restarting FastAPI..."}
    return await call_next(request)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis_router)
app.include_router(ask_router)
app.include_router(health_router)
app.include_router(data_router)

@app.get("/test")
async def test():
    return {"hello": "world"}


# from fastapi import FastAPI, Request
# from fastapi.responses import StreamingResponse
# from typing import List, AsyncGenerator

# from tools import async_fetch_compare, async_fetch_heatmap, async_fetch_monthly, async_fetch_daily, async_fetch_now, async_fetch_fakultas, async_fetch_gedung, async_fetch_lantai
# import csv
# import json

# from datetime import datetime, timedelta

# from fastapi.middleware.cors import CORSMiddleware


# from fastapi.responses import FileResponse

# from ask_analysis_pipeline import AskAnalysisPipeline
# from mas_llm.actions.analyze_page import AnalyzePage

# HOST_URL = "127.0.0.1:8000"

# app = FastAPI()

# analyze_page = AnalyzePage()

# example_mode = False

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000", "http://localhost:3001"],  
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# def progress_generator(progress, message):
#     yield f"data: {{\"status\": \"{message}\", \"progress\": {progress}}}\n\n"

# async def progress_stream(ask_analysis_pipeline, prompt) -> AsyncGenerator[str, None]:
#     """Generate a stream of progress events"""
#     yield "data: {\"status\": \"Analyzing request...\", \"progress\": 0}\n\n"
#     await ask_analysis_pipeline.set_progress_callback(progress_generator)
    
#     result = await ask_analysis_pipeline.run(prompt)
    
#     # Process result data
#     for res in result:
#         data = []
#         if res["data_dir"] == "":
#             res["data"] = data
#             continue
        
#         with open(res["data_dir"]) as csvf:
#             csvReader = csv.DictReader(csvf)
#             for rows in csvReader:
#                 data.append(rows)
#         res["data"] = data
#         del res["data_dir"]
    
#     # Send the final result
#     yield f"data: {{\"status\": \"Finalization complete\", \"progress\": 100, \"result\": {json.dumps(result)}}}\n\n"

# @app.get("/api/web/stream")
# async def web_api_stream(prompt):
#     ask_analysis_pipeline = AskAnalysisPipeline(source="web", example_mode=example_mode)
#     return StreamingResponse(
#         progress_stream(ask_analysis_pipeline, prompt),
#         media_type="text/event-stream"
#     )

# @app.post("/api/web")
# async def web_api(prompt):
#     ask_analysis_pipeline = AskAnalysisPipeline(source="web", example_mode=example_mode)
#     result = await ask_analysis_pipeline.run(prompt)

#     for res in result:
#         data = []
#         if res["data_dir"] == "":
#             res["data"] = data
#             continue
        
#         with open(res["data_dir"]) as csvf:
#             csvReader = csv.DictReader(csvf)
#             for rows in csvReader:
#                 data.append(rows)
#         res["data"] = data
#         del res["data_dir"]

#     return result

# @app.post("/api/line")
# async def line_api(prompt):
#     ask_analysis_pipeline = AskAnalysisPipeline(source="line", example_mode=example_mode)
#     result = await ask_analysis_pipeline.run(prompt)

#     for res in result:
#         res["image_url"] = res["image_dir"].replace("data/output/images/", f"{HOST_URL}/image/")
#         del res["image_dir"]

#     return result

# @app.post("/api/whatsapp")
# async def whatsapp_api(prompt):
#     ask_analysis_pipeline = AskAnalysisPipeline(source="whatsapp", example_mode=example_mode)
#     result = await ask_analysis_pipeline.run(prompt)

#     for res in result:
#         res["image_url"] = res["image_dir"].replace("data/output/images/", f"{HOST_URL}/image/")
#         del res["image_dir"]

#     return result


# @app.get("/image/{image_id}")
# async def get_image(image_id: str):
#     return FileResponse(f"data/output/{image_id}.png", media_type="image/png")

# #  Analysis per Page

# @app.get("/api/analysis/faculty")
# async def get_faculty_analysis(date: str):
#     data = await async_fetch_compare(date)

#     date_in_datetime = datetime.strptime(date, "%Y-%m")
#     past_month_in_datetime = date_in_datetime.replace(day=1) - timedelta(days=1)

#     past_month = past_month_in_datetime.strftime("%Y-%m")

#     history = await async_fetch_compare(past_month)

#     result = await analyze_page.run("compare_faculty", json.dumps(data), json.dumps(history))
#     return result


# @app.get("/api/analysis/heatmap")
# async def get_monthly_analysis(start: str, end: str, faculty: str = None, building: str = None):
#     data = await async_fetch_heatmap(start, end, faculty, building)

#     start_date_in_datetime = datetime.strptime(start, "%Y-%m-%d")
#     end_date_in_datetime = datetime.strptime(end, "%Y-%m-%d")

#     past_week_start_in_datetime = start_date_in_datetime - timedelta(days=7)
#     past_week_end_in_datetime = end_date_in_datetime - timedelta(days=7)

#     past_week_start = past_week_start_in_datetime.strftime("%Y-%m-%d")
#     past_week_end = past_week_end_in_datetime.strftime("%Y-%m-%d")

#     history = await async_fetch_heatmap(past_week_start, past_week_end, faculty, building)
    
#     result = await analyze_page.run("heatmap", json.dumps(data), json.dumps(history))
#     return result

# @app.get("/api/analysis/now")
# async def get_now_analysis(date: str, faculty: str = "", bulding: str = "", floor: str = ""):
#     data = await async_fetch_now(date, faculty, bulding, floor)
    
#     date_in_datetime = datetime.strptime(date, "%Y-%m-%d")    
#     past_week_in_datetime = date_in_datetime - timedelta(days=7)
    
#     history = await async_fetch_heatmap(past_week_in_datetime.strftime("%Y-%m-%d"), date, faculty, bulding)
   
#     result = await analyze_page.run("now", json.dumps(data), json.dumps(history))
#     print("Result" + result)
#     return result

# @app.get("/api/analysis/daily")
# async def get_daily_analysis(date: str, faculty: str = "", bulding: str = "", floor: str = ""):
#     data = await async_fetch_daily(date, faculty, bulding, floor)
    
#     date_in_datetime = datetime.strptime(date, "%Y-%m-%d")    
#     past_week_in_datetime = date_in_datetime - timedelta(days=7)
    
#     history = await async_fetch_heatmap(past_week_in_datetime.strftime("%Y-%m-%d"), date, faculty, bulding)
    
#     result = await analyze_page.run("daily", json.dumps(data), json.dumps(history))
#     print("Result" + result)
#     return result

# @app.get("/api/analysis/monthly")
# async def get_monthly_analysis(date: str, faculty: str = "", bulding: str = "", floor: str = ""):
#     data = await async_fetch_monthly(date, faculty, bulding, floor)
    
#     history = []
#     year_string = date.split("-")[0]
#     month_string = date.split("-")[1]
#     for i in range(0, 3):
#         month = int(month_string) - i
#         if month <= 0:
#             month += 12
#             year = int(year_string) - 1
#         else:
#             year = int(year_string)
        
#         if month < 10:
#             month_string = f"0{month}"
#         else:
#             month_string = str(month)
        
#         history_data = await async_fetch_monthly(f"{year}-{month_string}", faculty, bulding, floor)
#         history.append(history_data)
        
#     result = await analyze_page.run("monthly", json.dumps(data), json.dumps({}))
    
#     return result


# @app.get("/api/list/fakultas")
# async def get_faculty():
#     data = await async_fetch_fakultas()
#     return data


# @app.get("/api/list/gedung")
# async def get_gedung(faculty: str):
#     data = await async_fetch_gedung(faculty)
#     return data

# @app.get("list/lantai")
# async def get_gedung(faculty: str = None, bulding: str = None):
#     data = await async_fetch_lantai(faculty, bulding)
#     return data