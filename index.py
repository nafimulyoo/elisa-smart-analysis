from fastapi import FastAPI
from api_model import PromptRequest
from typing import List
import csv
import json

from fastapi.responses import FileResponse

from pipeline import Pipeline

HOST_URL = "127.0.0.1:8000"

app = FastAPI()

example_mode = False

@app.post("/api/web")
async def web_api(request: PromptRequest):
    pipeline = Pipeline(source="web", example_mode=example_mode)
    result = await pipeline.run(request)

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
async def line_api(request: PromptRequest):
    pipeline = Pipeline(source="line", example_mode=example_mode)
    result = await pipeline.run(request)

    for res in result:
        res["image_url"] = res["image_dir"].replace("data/output/images/", f"{HOST_URL}/image/")
        del res["image_dir"]

    return result

@app.post("/api/whatsapp")
async def whatsapp_api(request: PromptRequest):
    pipeline = Pipeline(source="whatsapp", example_mode=example_mode)
    result = await pipeline.run(request)

    for res in result:
        res["image_url"] = res["image_dir"].replace("data/output/images/", f"{HOST_URL}/image/")
        del res["image_dir"]

    return result


@app.get("/image/{image_id}")
async def get_image(image_id: str):
    return FileResponse(f"data/output/{image_id}.png", media_type="image/png")