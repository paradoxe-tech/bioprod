import sys
from sandbox.executor import DockerExecutor
from sandbox.security import CommandValidator
from sandbox.interface import LLMInterface
from sandbox.logger import setup_logger
from utils.config import load_config
from utils.prompt import prompt
from model.toolset import setup_toolset
import importlib
from langchain_core.tools import tool
from utils.tree import tree

import json

class Main:
    def __init__(self, filepath: str = "config/config.json"):
        self.verbose = True
        self.config = load_config(filepath)
        self.logger = setup_logger(self.config['logging'])
        self.toolset = setup_toolset(self.config['llm']["toolset"])
        self.executor = DockerExecutor(self.config['docker'], self.config['llm'])
        self.validator = CommandValidator(self.config['security'], self.toolset)
        self.interface = LLMInterface(self.config['llm'])
        
        use_online = self.config["llm"].get("use_online", False)
        module_name = "model.online" if use_online else "model.local"
        try:
            agent_module = importlib.import_module(module_name)
            self.agent = agent_module.Agent(self.config["llm"])
            self.logger.info(f"Using {'online' if use_online else 'local'} LLM agent")
        except ImportError as e:
            self.logger.error(f"Failed to import {module_name}: {str(e)}")
            raise

    def ask(self):
        if not sys.stdin.isatty():
            input = sys.stdin.read().strip()
        else:
            input = prompt("OpenBeing Bioprod Agent > ")

        output = self.agent.ask(input)

        thought = output.split("Thought:")[1].split("Response:")[0].strip()
        response = output.split("Response:")[1].split("Action:")[0].strip()
        action = output.split("Action:")[1].strip()

        # print in grey
        print("\033[90m" + thought + "\033[0m")
        print(response)

        try:
            action = json.loads(action)
            if action["type"] == "function" and action["name"] == "shell":
                command = action["parameters"]["command"]
                print("\033[90m $ " + command + "\033[0m")
                response = self.execute(command)
                print("\033[94m" + response + "\033[0m")
        except json.JSONDecodeError:
            self.logger.error("Failed to decode JSON action")


    def execute(self, input_str: str) -> str:
        """Execute a command in the workspace."""

        input = self.interface.parse(input_str)

        if not input["success"]:
            self.logger.error(f"Parsing error: {input['error']}")
            return "Parsing error"
        
        command = input.get("command", "")
        is_valid, command = self.validator.validate(command)

        if not is_valid:
            self.logger.error(f"Validation error: {command}")
            return "Validation error"
        
        execution = self.executor.run(command)
        response = self.interface.standardify(execution)
        
        if not response["success"]:
            self.logger.error(f"Execution error: {response['error']}")
            return "Execution error"
        
        return response['output']

if __name__ == "__main__":
    process = Main("config/config.json")
    
    while True:
        try:
            process.ask()
        except KeyboardInterrupt:
            print("\n" + tree(process.executor.list_files()))
            process.logger.info("\nExiting Bioprod.")
            break
        except Exception as e:
            process.logger.error(e)