import docker, re, os, io, tarfile
from typing import Dict, List, Union, Optional
from docker.models.containers import Container

class DockerExecutor:
    
    def __init__(self, docker_config: Dict):
        self.client = docker.from_env()
        self.image = docker_config.get("image", "alpine")
        self.constraints = {
            "remove": docker_config.get("remove", True),
            "network_disabled": docker_config.get("network_disabled", True),
            "mem_limit": docker_config.get("mem_limit", "64m"),
            "cpu_period": docker_config.get("cpu_period", 100000),
            "cpu_quota": docker_config.get("cpu_quota", 50000),
        }

        self.container: Optional[Container] = None
        self.start()

        for file in docker_config.get("copied_files", []):
            self.upload(file, "workspace")
    
    def run(self, command: Union[str, List[str]]) -> Dict:
        try:
            if self.container is None:
                return {
                    "success": False,
                    "output": None,
                    "error": "Container not started"
                }
            
            if isinstance(command, list):
                command = " ".join(command)
            
            exec_log = self.container.exec_run(f"sh -c 'cd /workspace && {command}'")
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

            self.container.exec_run("mkdir -p workspace")

    def list_files(self):
        if self.container is None:
            return {"error": "Container not started"}

        exec_log = self.container.exec_run(f"find workspace -type f")
        output = exec_log.output.decode().strip().split("\n")

        tree = {}
        for path in output:
            parts = path.strip("/").split("/")

            cursor = tree
            for part in parts[:-1]:
                cursor = cursor.setdefault(part, {})
            cursor[parts[-1]] = {}

        def to_tree(d):
            return [
                {
                    "name": key,
                    "children": to_tree(value) if value else None
                } for key, value in d.items()
            ]

        return to_tree(tree)


    def upload(self, src_path: str, dst_path: str):
        if self.container is None:
            return {"error": "Container not started"}

        tarstream = io.BytesIO()
        with tarfile.open(fileobj=tarstream, mode='w') as tar:
            tar.add(src_path, arcname=os.path.basename(src_path))
        tarstream.seek(0)

        self.container.put_archive(dst_path, tarstream)