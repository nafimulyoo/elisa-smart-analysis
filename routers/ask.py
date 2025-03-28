# app/routers/ask.py
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import csv
import json

from ask_analysis_pipeline import AskAnalysisPipeline
from config import settings

from typing import AsyncGenerator
from fastapi.responses import FileResponse

router = APIRouter(tags=["ask"]) #Added tags

example_mode = False  # Consider putting this in the config

def progress_generator(progress, message):
    yield f"data: {{\"status\": \"{message}\", \"progress\": {progress}}}\n\n"

async def progress_stream(ask_analysis_pipeline, prompt) -> AsyncGenerator[str, None]:
    """Generate a stream of progress events"""
    yield "data: {\"status\": \"Analyzing request...\", \"progress\": 0}\n\n"
    await ask_analysis_pipeline.set_progress_callback(progress_generator)

    result = await ask_analysis_pipeline.run(prompt)

    # Process result data
    for res in result:
        data = []
        if res["data_dir"] == "":
            res["data"] = data
            continue

        with open(res["data_dir"]) as csvf:
            csvReader = csv.DictReader(csvf)
            for rows in csvReader:
                data.append(rows)
        res["data"] = data
        del res["data_dir"]

    # Send the final result
    yield f"data: {{\"status\": \"Finalization complete\", \"progress\": 100, \"result\": {json.dumps(result)}}}\n\n"

@router.get("/api/web/stream")
async def web_api_stream(prompt):
    ask_analysis_pipeline = AskAnalysisPipeline(source="web", example_mode=example_mode)
    return StreamingResponse(
        progress_stream(ask_analysis_pipeline, prompt),
        media_type="text/event-stream"
    )

@router.post("/api/web")
async def web_api(prompt):
    ask_analysis_pipeline = AskAnalysisPipeline(source="web", example_mode=example_mode)
    result = await ask_analysis_pipeline.run(prompt)

    for res in result:
        data = []
        if res["data_dir"] == "":
            res["data"] = data
            continue

        with open(res["data_dir"]) as csvf:
            csvReader = csv.DictReader(csvf)
            for rows in csvReader:
                data.append(rows)
        res["data"] = data
        del res["data_dir"]

    return result

@router.post("/api/line")
async def line_api(prompt):
    ask_analysis_pipeline = AskAnalysisPipeline(source="line", example_mode=example_mode)
    result = await ask_analysis_pipeline.run(prompt)

    for res in result:
        res["image_url"] = res["image_dir"].replace("data/output/images/", f"{settings.host_url}/image/")
        del res["image_dir"]

    return result

@router.post("/api/whatsapp")
async def whatsapp_api(prompt):
    ask_analysis_pipeline = AskAnalysisPipeline(source="whatsapp", example_mode=example_mode)
    result = await ask_analysis_pipeline.run(prompt)

    for res in result:
        res["image_url"] = res["image_dir"].replace("data/output/images/", f"{settings.host_url}/image/")
        del res["image_dir"]

@router.get("/image/{image_id}")
async def get_image(image_id: str):
    return FileResponse(f"data/output/{image_id}.png", media_type="image/png")
