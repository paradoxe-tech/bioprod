from langchain_ollama import ChatOllama
import ollama
from typing import Dict

class Agent:

    def __init__(self, config: Dict, tools):
        self.config = config
        self.tools = tools
        self.model_name = self.config["model"]
        self.model = ChatOllama(model=self.model_name, verbose=False)

        self.messages = {
            "messages": [
                {
                    "role": "system",
                    "content": (
                "You are a bioproduction assistant specialized in molecular biology and "
                "biotechnology. Your tasks include:\n"
                "- Searching and retrieving DNA and protein sequences from trusted databases "
                "like NCBI and UniProt.\n"
                "- Explaining protocols and biological pathways.\n"
                "- Suggesting bioinformatics commands and pipelines.\n"
                "- Using available tools like shell commands or APIs when needed.\n"
                "- Provide concise, factual answers.\n"
                "Be collaborative and ask clarifying questions when unsure."
            )
                }
            ]
        }

    def ask(self, role: str, query: str) -> str:
        try:
            system_message = self.messages["messages"][0]["content"]
            
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": role, "content": query}
                ],
                options={
                    "num_predict": 512,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_ctx": 2048
                }
            )
            
            answer = response["message"]["content"]
            return answer
            
        except Exception as e:
            return f"Error: {str(e)}"