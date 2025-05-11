from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
# In your FastAPI app
import requests
import os


import os
import yaml

def create_config_file(config_data, file_path):
    """
    Writes a YAML configuration file to the specified path.

    Args:
        config_data (dict): A dictionary containing the configuration data.
        file_path (str): The path to the file where the configuration
                          should be written.
    """
    try:
        with open(file_path, 'w') as outfile:
            yaml.dump(config_data, outfile, default_flow_style=False)
        print(f"Configuration file created successfully at: {file_path}")
    except Exception as e:
        print(f"Error creating configuration file: {e}")

config_dir = "config"
if not os.path.exists(config_dir):
    os.makedirs(config_dir)

# Define the three different LLM models
llm_models = [
    ["google/gemini-2.0-flash-001", "config2"],
    ["google/gemini-2.5-flash-preview", "gemini-2.5"],
    ["deepseek/deepseek-r1-distill-llama-8b", "deepseek-r1"],
    ["google/gemma-3-4b-it", "gemma3"]
]

for i, model in enumerate(llm_models):
        config_file_name = f"{model[1]}.yaml"
        config_file_path = os.path.join(config_dir, config_file_name)

        # Configuration data (common to all files)
        config_data = {
            'llm': {
                'base_url': 'https://openrouter.ai/api/v1',
                'api_key': os.getenv('LLM_API_KEY', 'YOUR_LLM_API_KEY'),
                'model': model[0],
            },
            'embedding': {
                'api_type': 'gemini',
                'api_key': os.getenv('EMB_API_KEY', 'YOUR_EMB_API_KEY'),
                'dimensions': '1024',
                'model': 'text-embedding-004'
            }
        }

        # Write the configuration data to the file
        create_config_file(config_data, config_file_path)

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

