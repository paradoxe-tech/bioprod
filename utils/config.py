import os, sys, json
from typing import Dict

def load_config(filepath) -> Dict:
    try:
        with open(filepath, 'r') as config_file:
            return json.load(config_file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading the config: {str(e)}")
        sys.exit(1)