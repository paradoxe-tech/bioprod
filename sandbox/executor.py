import docker
from typing import Dict, List, Union

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
    
    def run(self, command: Union[str, List[str]]) -> Dict:
        try:
            output = self.client.containers.run(
                image=self.image,
                command=command,
                stdout=True,
                stderr=True,
                remove=self.constraints["remove"],
                network_disabled=self.constraints["network_disabled"],
                mem_limit=self.constraints["mem_limit"],
                cpu_period=self.constraints["cpu_period"],
                cpu_quota=self.constraints["cpu_quota"],
            )
            return {
                "success": True,
                "output": output.decode(),
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "output": None,
                "error": str(e)
            }