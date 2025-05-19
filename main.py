import sys, importlib, json
from typing import List
from sandbox.executor import DockerExecutor
from sandbox.security import CommandValidator
from sandbox.interface import LLMInterface
from sandbox.logger import setup_logger
from utils.config import load_config
from utils.prompt import prompt
from utils.tree import tree
from utils.parser import parse_output
from model.toolset import setup_toolset

class Main:
    def __init__(self, filepath: str = "config/config.json"):
        self.verbose = True
        self.config = load_config(filepath)
        self.logger = setup_logger(self.config['logging'])
        self.toolset = setup_toolset(self.config['llm']["toolset"])
        self.executor = DockerExecutor(self.config['docker'])
        self.validator = CommandValidator(self.config['security'], self.toolset)
        self.interface = LLMInterface(self.config['llm'])
        self.executed = []
        
        use_online = self.config["llm"].get("use_online", False)
        module_name = "model.online" if use_online else "model.local"
        try:
            agent_module = importlib.import_module(module_name)
            self.agent = agent_module.Agent(self.config["llm"]) if use_online else agent_module.Agent(self.config["llm"], self.toolset)
        except ImportError as e:
            self.logger.error(f"Failed to import {module_name}: {str(e)}")
            raise

    def ask(self, question = None) -> List[str]:
        if __name__ == "__main__":
            if not sys.stdin.isatty():
                input = sys.stdin.read().strip()
            else:
                if question:
                    input = prompt(question + " > ")
                else:
                    input = prompt("Ask Agent > ")

            return self.query("user", input)
        
        return [question] if question else []
        
    def query(self, role: str, input: str, stack = 0) -> List[str]:

        if stack > 5:
            self.logger.error("Stack overflow detected.")
            return [f"! The model is not able to iterate more than {self.config['llm']['max_iterations']} times."]

        output = self.agent.ask(role, input)
        thought, response, action = parse_output(output)

        if output.startswith("{") and output.endswith("}"):
            action = output
            response = ""

        if stack == 0:
            self.executed = []

        try:    
            action = json.loads(action)
            
            if action["name"] == "end":
                return [response] + self.ask()
            
            if action["name"] == "ask":
                return [response] + self.ask(action["parameters"]["value"])
            
            if action["name"] == "shell":
                command = action["parameters"]["value"]

                if stack > 0 and command in self.executed:
                    self.logger.error(f"Command already executed: {command}")
                    next = self.query("user", f"""Your previous action ({command}) was rejected because it has already been executed.
                    Your task is to answer the question: {input}""", stack + 1)

                    return [response, f"$ {command}", "! This command has already been executed."] + next
                
                output = self.execute(command, stack)
                next = self.query("user", f"""Here is the result of you previous action ({command}):
                    {output}.\n Your task is to answer the question: {input}""", stack + 1)

                return [response, f"$ {command}"] + next
                
        except json.JSONDecodeError:
            pass
        
        return [response] + self.ask()

    def execute(self, input_str: str, stack = 0) -> str:
        """Execute a command in the workspace."""

        input = self.interface.parse(input_str)

        if not input["success"]:
            self.logger.error(f"Parsing error: {input['error']}")
            return "Parsing error: the format of the action is incorrect."
        
        command = input.get("command", "")
        is_valid, command = self.validator.validate(command)

        if not is_valid:
            self.logger.error(f"Validation error: {command}")
            return "Validation error: {command} is not allowed."
        
        execution = self.executor.run(command)
        self.executed.append(command)
        response = self.interface.standardify(execution)
        
        if not response["success"]:
            self.logger.error(f"Execution error: {response['error']}")
            return "Execution error: {response['error']}"
        
        return response['output']