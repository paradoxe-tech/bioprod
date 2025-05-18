# BioProd Agent

A bioproduction agent specialized in molecular biology and biotechnology tasks. Able to run command inside of a docker container, which allows it to use every biotool available.

for a quick overview of the output results, see [https://biomera-view.replit.app/](https://biomera-view.replit.app/) !

## Installation

### Local Model Setup (Default)

First, get ollama and pull the model you want:

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull mistral
```

### Online Model Setup

To use online models that support function calling (like OpenAI models), set the following environment variables:

```bash
export OPENAI_API_KEY="your_api_key_here"
# Optional: For other OpenAI-compatible providers like Anyscale or Together.ai
# export OPENAI_API_BASE="https://api.together.xyz/v1"
```

Then activate online mode by editing `config/config.json` and setting:
```json
"use_online": true
```

### Docker Setup

Then, get docker (some help is available [here](https://docs.docker.com/engine/install/)) and activate it for WSL if you're planning to run under windows subsystem for Linux.

### Python Dependencies

Finally, install the python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the agent with:

```bash
python main.py
```
