from fastapi import APIRouter

import requests
import os

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
async def health_check(object=None):
    if object == "elisa":
        url = f"https://elisa.itb.ac.id/api/now?date=2025-01-01&faculty=&building=&floor="
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            return {"status": "OK"}
        else:
            return {"status": "failed"}
    return {"status": "OK"}

