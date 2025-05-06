# app/routers/analysis.py
from fastapi import APIRouter, Depends, HTTPException, status
import asyncio
from typing import Annotated
from datetime import datetime, timedelta
from utils.model import model_list, generate_yaml_config, get_model_from_config


settings_router = APIRouter(prefix="/api", tags=["model"])

@settings_router.get("/model")
# @profile_endpoint()
async def get_model():
    return {
        "model": get_model_from_config(),
    }

@settings_router.post("/model")
# @profile_endpoint()
async def set_model(model: str):
    # check if the model is in the list
    if model not in model_list:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Model {model} is not supported. Supported models are: {list(model_list.keys())}"
        )
    # Generate the YAML config
    generate_yaml_config(model)
    # Load the config
    model = get_model_from_config()

    return {
        "model": model,
        "message": f"Model set to {model}"
    }
