from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
# In your FastAPI app

import os
from pathlib import Path
import yaml


import requests
# try:
#     print("Checking VPN connection... -- FROM PYTHON")
#     response = requests.get("https://elisa.itb.ac.id")
#     if response.status_code == 200:
#         print("VPN connection is working, ping elisa.itb.ac.id -- FROM PYTHON")
#     else:
#         print("VPN connection is not working")
# except requests.exceptions.RequestException as e:   
#     print(f"VPN connection is not working: {e}")


def generate_yaml_config():
    """Generate config.yaml with LLM and embedding settings from environment variables"""
    print("Generating YAML config...")
    config = {
        'llm': {
            'api_type': os.getenv('LLM_API_TYPE', 'gemini'),
            'api_key': os.getenv('LLM_API_KEY', ''),
            'model': os.getenv('LLM_MODEL', 'gemini-2.0-flash'),
            'max_token': int(os.getenv('LLM_MAX_TOKEN', '2048'))
        },
        'embedding': {
            'api_type': os.getenv('EMB_API_TYPE', 'gemini'),
            'api_key': os.getenv('EMB_API_KEY', ''),
            'dimensions': os.getenv('EMB_DIMENSIONS', '1024'),
            'model': os.getenv('EMB_MODEL', 'text-embedding-004')
        }
    }

    print("Config generated:")
    print(config)
    # Write YAML file
    config_path = Path('config/config2.yaml')
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    print(f"YAML config generated at: {config_path.absolute()}")

generate_yaml_config()
app = FastAPI()


from routers.ask import ask_router
from routers.analysis import analysis_router
from routers.health import health_router
from routers.data import data_router

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

