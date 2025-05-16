from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from typing import Dict

class Agent:

    def __init__(self, config: Dict, tools):
        self.config = config
        self.tools = tools
        self.model = ChatOllama(model=self.config["model"], verbose=True)
        self.agent = create_react_agent(
            model=self.model, 
            tools=self.tools,
        )

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

    def ask(self, query: str) -> str:
        self.messages["messages"].append({"role": "user", "content": query})

        response = self.agent.invoke({"messages": self.messages["messages"]})
        answer = response["messages"][-1].content

        self.messages["messages"].append({"role": "assistant", "content": answer})

        return answer