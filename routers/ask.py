# app/routers/ask.py
from fastapi import APIRouter
import csv

from ask_analysis_pipeline import AskAnalysisPipeline

import psutil
from loguru import logger as log

from fastapi.responses import FileResponse

from functools import wraps
import time

ask_router = APIRouter(tags=["ask"]) #Added tags

image_host_url = "http://localhost:8000/image"
example_mode = False  # Consider putting this in the config

web_pipeline = AskAnalysisPipeline(source="web", example_mode=example_mode)
line_pipeline = AskAnalysisPipeline(source="line", example_mode=example_mode)
whatsapp_pipeline = AskAnalysisPipeline(source="whatsapp", example_mode=example_mode)

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


@ask_router.get("/api/web")
# @profile_endpoint()
async def web_api(prompt, model=""):
    print("Prompt received:", prompt)
    print("Model received:", model)
    result, notebook = await web_pipeline.run(prompt, model)

    for res in result:
        if res["visualization_type"] != "":
            data = []
            if res["data_dir"] == "":
                res["data"] = []
                continue

            try:
                with open(res["data_dir"]) as csvf:
                    csvReader = csv.DictReader(csvf)
                    for rows in csvReader:
                        data.append(rows)
                res["data"] = data
            except Exception as e:
                log.error(f"Error reading CSV file: {e}")
                res["data"] = []
            
            del res["data_dir"]
    log_file_path = f"memory.log"
    log.add(log_file_path, level="INFO", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
    log.info("MEMORY: " + str(psutil.virtual_memory()))
    log.remove() 

    return {
        "result": result,
        "notebook": notebook,
    }

@ask_router.get("/api/line")
# @profile_endpoint()
async def line_api(prompt):

    result = await line_pipeline.run(prompt)

    for res in result:
        res["image_url"] = res["image_dir"].replace("data/output/images/", f"{image_host_url}/image/")
        del res["image_dir"]

    return result

@ask_router.get("/api/whatsapp")
async def whatsapp_api(prompt):
    result = await whatsapp_pipeline.run(prompt)

    for res in result:
        res["image_url"] = res["image_dir"].replace("data/output/images/", f"{image_host_url}/image/")
        del res["image_dir"]

@ask_router.get("/image/{image_id}")
# @profile_endpoint()
async def get_image(image_id: str):
    return FileResponse(f"data/output/{image_id}.png", media_type="image/png")
