from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
# In your FastAPI app
import requests
import os


from utils.model import model_list, generate_yaml_config # type: ignore

# import requests
# try:
#     print("Checking VPN connection... -- FROM PYTHON")
#     response = requests.get("https://elisa.itb.ac.id")
#     if response.status_code == 200:
#         print("VPN connection is working, ping elisa.itb.ac.id -- FROM PYTHON")
#     else:
#         print("VPN connection is not working")
# except requests.exceptions.RequestException as e:   
#     print(f"VPN connection is not working: {e}")



# generate_yaml_config("llama_open")

app = FastAPI()


from routers.ask import ask_router
from routers.analysis import analysis_router
from routers.health import health_router
from routers.data import data_router
from routers.settings import settings_router

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis_router)
app.include_router(ask_router)
app.include_router(health_router)
app.include_router(data_router)
app.include_router(settings_router)

@app.get("/test-self")
async def test():
    return {"hello": "world"}

@app.get("/test-elisa")
async def test():
    try:
        response = requests.get("https://elisa.itb.ac.id")
        if response.status_code == 200:
            return {"status": "VPN connection is working"}
        else:
            return {"status": "VPN connection is not working"}
    except requests.exceptions.RequestException as e:   
        return {"status": f"VPN connection is not working: {e}"}

