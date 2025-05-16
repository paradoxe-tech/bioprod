from typing import Dict, Any

class LLMInterface:

    def __init__(self, config: Dict):
        self.format_version = config.get("format_version", "1.0")
        self.expected_keys = config.get("expected_keys", ["command"])
    
    def parse(self, command: str) -> Dict[str, Any]:
        try:
            command = command if isinstance(command, str) else " ".join(command)
            return {
                "success": True,
                "command": command,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "parsed": None,
                "error": f"Parsing error: {str(e)}"
            }
    
    def standardify(self, output: Dict) -> Dict:
        return {
            "success": output.get("success"),
            "output": output.get("output"),
            "error": output.get("error"),
            "format_version": self.format_version
        }