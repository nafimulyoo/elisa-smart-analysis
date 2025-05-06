import os
from pathlib import Path
import yaml

config_path = Path('config/config2.yaml')

model_list = {
    "gemini": {
        'api_type': 'gemini',
        'api_key': os.getenv('LLM_API_KEY', ''),
        'model': 'gemini-2.0-flash',
        'max_token': 2048
    },
    "llama": {
        'api_type': 'ollama',
        # 'base_url': 'http://192.168.10.46:11434/api',
        'base_url': 'http://localhost:11434/api',
        'model': 'llama3.2',
        'max_token': 2048
    },
    "gemma": {
        'api_type': "ollama",
        # 'base_url': "http://192.168.10.46:11434/api",
        'model': "gemma",
        'max_token': 2048
    },
    "llama_open": {
        'api_type': 'openrouter',
        'base_url': 'https://openrouter.ai/api/v1',
        'api_key': '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',
        'model': 'meta-llama/llama-3.2-3b-instruct:free'
    }
}



def generate_yaml_config(model: str = "gemini"):
    """Generate config.yaml with LLM and embedding settings from environment variables"""
    print("Generating YAML config...")
    # Check if the model is in the list
    if model not in model_list:
        raise ValueError(f"Model {model} is not supported. Supported models are: {list(model_list.keys())}")
    # Get the model configuration
    model_config = model_list[model]
    config = {
        'llm': model_config,
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
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    print(f"YAML config generated at: {config_path.absolute()}")


def get_model_from_config():
    """Load config.yaml and return as dictionary"""
    
    if not config_path.exists():
        raise FileNotFoundError(f"Config file {config_path} does not exist.")
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    model_name = config['llm']['model']
    return model_name