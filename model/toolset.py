import sys, json
from typing import Dict

def setup_toolset(path: str) -> Dict:

    try:
        with open(path, "r") as file:
            toolset = json.load(file)
            return toolset
        
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading the toolset: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)

    return {}