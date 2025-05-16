import shlex
from typing import List, Dict, Tuple, Union

class CommandValidator:
 
    def __init__(self, config: Dict):

        self.allowed_commands = config.get("allowed_commands", [])
        self.allowed_flags = config.get("allowed_flags", {})
        self.blocked_patterns = config.get("blocked_patterns", [])
    
    def validate(self, command: str) -> Tuple[bool, Union[List[str], str]]:
        try:
            parsed = shlex.split(command)
            
            if not parsed:
                return False, "Empty command"
                
            base_command = parsed[0]
            if base_command not in self.allowed_commands:
                return False, f"Unauthorized command: {base_command}"
            
            for pattern in self.blocked_patterns:
                if pattern in command:
                    return False, f"Forbidden pattern detected: {pattern}"
            
            return True, parsed
            
        except Exception as e:
            return False, f"Erreur de validation: {str(e)}"