# BioProd Agent

The first bioproduction AI agent, specialized in molecular biology and biotechnology tasks. It allows for task automation and neophyte usage of complex tools, by leveraging various pipelines to collect data, design pathways, run analysis, enhance molecules and so much more. Technically, it is able to run command inside of a docker container, which allows it to use every biotool available.

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
export FIREWORKS_API_KEY="your_api_key_here"
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
