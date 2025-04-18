from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
# In your FastAPI app
import psutil
import os
from pathlib import Path
import yaml

# from vpn_itb.openvpnclient import OpenVPNClient


# vpn = OpenVPNClient("./vpn_itb/itb-2022-mac.ovpn", connect_timeout=15)
# try:
#     vpn.disconnect()
# except Exception as e:
#     print(f"Failed to disconnect from VPN: {e}")
# try:
#     vpn.connect()
#     os.system("ping -c 4 elisa.itb.ac.id")
# except Exception as e:
#     print(f"Failed to connect to VPN: {e}")

# os.system("ping -c 4 elisa.itb.ac.id")

# run vpn_conncect.sh
# os.system("bash vpn_connect.sh")

import requests
try:
    print("Checking VPN connection... -- FROM PYTHON")
    response = requests.get("https://elisa.itb.ac.id")
    if response.status_code == 200:
        print("VPN connection is working, ping elisa.itb.ac.id -- FROM PYTHON")
    else:
        print("VPN connection is not working")
except requests.exceptions.RequestException as e:   
    print(f"VPN connection is not working: {e}")


def generate_yaml_config():
    """Generate config.yaml with LLM and embedding settings from environment variables"""
    
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

    # Write YAML file
    config_path = Path('config/config2.yaml')
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    print(f"YAML config generated at: {config_path.absolute()}")

generate_yaml_config()

from routers.ask import ask_router
from routers.analysis import analysis_router
from routers.health import health_router
from routers.data import data_router

from config import settings


app = FastAPI()


def kill_fastapi_processes():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'fastapi' in ' '.join(proc.info['cmdline'] or []):
            proc.kill()

@app.middleware("http")
async def restart_on_memory_limit(request, call_next):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == "ipykernel_launcher":
            proc.kill()
#     if psutil.virtual_memory().percent > 80: 
#         kill_fastapi_processes()
#         os.system("fast run index.py")
#         return {"message": "Restarting FastAPI..."}
    return await call_next(request)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis_router)
app.include_router(ask_router)
app.include_router(health_router)
app.include_router(data_router)

@app.get("/test")
async def test():
    return {"hello": "world"}

