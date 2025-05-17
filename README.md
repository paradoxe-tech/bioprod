# Installation

First, get ollama and pull the model you want. It needs to s tool-embedding.

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1
```

Then, get docker (some help is available [here](https://docs.docker.com/engine/install/)) and activate it for WSL if you're planning to run under windows subsystem for Linux.

Finally, install the python dependencies.

```bash
pip install -r requirements.txt
```