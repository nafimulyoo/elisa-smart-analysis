from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from typing import List, AsyncGenerator
import csv
import json

from fastapi.middleware.cors import CORSMiddleware


from fastapi.responses import FileResponse

from pipeline import Pipeline

HOST_URL = "127.0.0.1:8000"

app = FastAPI()

example_mode = False

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def progress_generator(progress, message):
    yield f"data: {{\"status\": \"{message}\", \"progress\": {progress}}}\n\n"

async def progress_stream(pipeline, prompt) -> AsyncGenerator[str, None]:
    """Generate a stream of progress events"""
    yield "data: {\"status\": \"Analyzing request...\", \"progress\": 0}\n\n"
    await pipeline.set_progress_callback(progress_generator)
    
    result = await pipeline.run(prompt)
    
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

@app.get("/api/web/stream")
async def web_api_stream(prompt):
    pipeline = Pipeline(source="web", example_mode=example_mode)
    return StreamingResponse(
        progress_stream(pipeline, prompt),
        media_type="text/event-stream"
    )

@app.post("/api/web")
async def web_api(prompt):
    pipeline = Pipeline(source="web", example_mode=example_mode)
    result = await pipeline.run(prompt)

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

@app.post("/api/line")
async def line_api(prompt):
    pipeline = Pipeline(source="line", example_mode=example_mode)
    result = await pipeline.run(prompt)

    for res in result:
        res["image_url"] = res["image_dir"].replace("data/output/images/", f"{HOST_URL}/image/")
        del res["image_dir"]

    return result

@app.post("/api/whatsapp")
async def whatsapp_api(prompt):
    pipeline = Pipeline(source="whatsapp", example_mode=example_mode)
    result = await pipeline.run(prompt)

    for res in result:
        res["image_url"] = res["image_dir"].replace("data/output/images/", f"{HOST_URL}/image/")
        del res["image_dir"]

    return result


@app.get("/image/{image_id}")
async def get_image(image_id: str):
    return FileResponse(f"data/output/{image_id}.png", media_type="image/png")