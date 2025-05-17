import docker
from typing import Dict, List, Union, Optional
from docker.models.containers import Container

class DockerExecutor:
    
    def __init__(self, config: Dict):
        self.client = docker.from_env()
        self.image = config.get("image", "alpine")
        self.constraints = {
            "remove": config.get("remove", True),
            "network_disabled": config.get("network_disabled", True),
            "mem_limit": config.get("mem_limit", "64m"),
            "cpu_period": config.get("cpu_period", 100000),
            "cpu_quota": config.get("cpu_quota", 50000),
        }

        self.container: Optional[Container] = None
        self.start()
    
    def run(self, command: Union[str, List[str]]) -> Dict:
        try:
            if self.container is None:
                return {
                    "success": False,
                    "output": None,
                    "error": "Container not started"
                }
            
            exec_log = self.container.exec_run(command)
            output = exec_log.output.decode()

            return {
                "success": True,
                "output": output,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "output": None,
                "error": str(e)
            }
        
    def start(self):
        if self.container is None:
            self.container = self.client.containers.run(
                image=self.image,
                command="sleep infinity",
                detach=True,
                remove=self.constraints["remove"],
                network_disabled=self.constraints["network_disabled"],
                mem_limit=self.constraints["mem_limit"],
                cpu_period=self.constraints["cpu_period"],
                cpu_quota=self.constraints["cpu_quota"],
            )