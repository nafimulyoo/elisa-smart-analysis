from fastapi import FastAPI
from api_model import PromptRequest, AnalysisResultWeb, AnalysisResultLINE, AnalysisResultWhatsApp
from typing import List

from pipeline import Pipeline

app = FastAPI()

example_mode = False

@app.post("/api/web", response_model=List[AnalysisResultWeb])
async def web_api(request: PromptRequest):
    pipeline = Pipeline(source="web", example_mode=example_mode)
    result = await pipeline.run(request)

    return result

@app.post("/api/line", response_model=List[AnalysisResultLINE])
async def line_api(request: PromptRequest):
    pipeline = Pipeline(source="line", example_mode=example_mode)
    result = await pipeline.run(request)

    return result

@app.post("/api/whatsapp", response_model=List[AnalysisResultWhatsApp])
async def whatsapp_api(request: PromptRequest):
    pipeline = Pipeline(source="whatsapp", example_mode=example_mode)
    result = await pipeline.run(request)

    return result