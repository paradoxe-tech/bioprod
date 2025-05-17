import sys
from sandbox.executor import DockerExecutor
from sandbox.security import CommandValidator
from sandbox.interface import LLMInterface
from sandbox.logger import setup_logger
from utils.config import load_config
from utils.prompt import prompt
from model.core import Agent
from model.toolset import setup_toolset
from langchain_core.tools import tool

from utils.tree import tree

def debug(message: str):
    """Shell executor that runs in sandboxed terminal."""
    print(f"[DEBUG] {message}")
    return "Command was executed correctly."

class Main:
    def __init__(self, filepath: str = "config/config.json"):
        self.verbose = True
        self.config = load_config(filepath)
        self.logger = setup_logger(self.config['logging'])
        self.toolset = setup_toolset(self.config['llm']["toolset"])
        self.executor = DockerExecutor(self.config['docker'], self.config['llm'])
        self.validator = CommandValidator(self.config['security'], self.toolset)
        self.interface = LLMInterface(self.config['llm'])
        self.agent = Agent(self.config["llm"], [debug])

    def ask(self):
        if not sys.stdin.isatty():
            input = sys.stdin.read().strip()
        else:
            input = prompt("OpenBeing Bioprod Agent > ")

        output = self.agent.ask(input)

        print(output)

    @tool
    def execute(self, input_str: str) -> str:
        """Execute a command in a Docker container."""

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