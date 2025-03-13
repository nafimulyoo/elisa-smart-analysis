from fastapi import FastAPI, HTTPException
from api_model import PromptRequest, AnalysisResultWeb, AnalysisResultLINE, AnalysisResultWhatsApp
from typing import List

app = FastAPI()

example_mode = True

@app.post("/api/web", response_model=List[AnalysisResultWeb])
async def web_api(request: PromptRequest):
    results = []

    if example_mode: 
        results = [
            AnalysisResultWeb(
                data={"example_key": "example_value"},
                visualization_type="bar_chart",
                explanation="1. This is an example explanation for the analysis."
            ),
            AnalysisResultWeb(
                data={"example_key": "example_value"},
                visualization_type="line_chart",
                explanation="2. This is an example explanation for the analysis."
            ),
        ]
    return results

@app.post("/api/line", response_model=List[AnalysisResultLINE])
async def line_api(request: PromptRequest):
    results = []

    if example_mode:
        results = [
            AnalysisResultLINE(
                data={"example_key": "example_value"},
                image_url="https://example.com/image.png",
                explanation="1. This is an example explanation for the LINE analysis."
            ),
            AnalysisResultLINE(
                data={"example_key": "example_value"},
                image_url="https://example.com/image.png",
                explanation="2. This is an example explanation for the LINE analysis."
            )
        ]

    return results

@app.post("/api/whatsapp", response_model=List[AnalysisResultWhatsApp])
async def whatsapp_api(request: PromptRequest):
    results = []

    if example_mode:
        results = [
            AnalysisResultWhatsApp(
                data={"example_key": "example_value"},
                image_url="https://example.com/image.png",
                explanation="1. This is an example explanation for the WhatsApp analysis."
            ),
            AnalysisResultWhatsApp(
                data={"example_key": "example_value"},
                image_url="https://example.com/image.png",
                explanation="2. This is an example explanation for the WhatsApp analysis."
            )
        ]
    return results
