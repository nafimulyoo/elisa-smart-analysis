import os
import yaml
from pathlib import Path

def generate_yaml_config():
    """Generate config.yaml with LLM and embedding settings from environment variables"""
    
    config = {
        'llm': {
            'api_type': os.getenv('LLM_API_TYPE', 'gemini'),
            'api_key': os.getenv('LLM_API_KEY', 'AIzaSyBtS1Db2S-H1Rx4Sl2UeOBtltYy_ta5cw4'),
            'model': os.getenv('LLM_MODEL', 'gemini-2.0-flash'),
            'max_token': int(os.getenv('LLM_MAX_TOKEN', '2048'))
        },
        'embedding': {
            'api_type': os.getenv('EMB_API_TYPE', 'gemini'),
            'api_key': os.getenv('EMB_API_KEY', 'AIzaSyBtS1Db2S-H1Rx4Sl2UeOBtltYy_ta5cw4'),
            'dimensions': os.getenv('EMB_DIMENSIONS', '1024'),
            'model': os.getenv('EMB_MODEL', 'text-embedding-004')
        }
    }

    # Write YAML file
    config_path = Path('config/config2.yaml')
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    print(f"YAML config generated at: {config_path.absolute()}")

if __name__ == '__main__':
    generate_yaml_config()