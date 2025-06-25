# crewai-weather-mcp-agent

A CrewAI-powered multi-agent system that connects with the [weather MCP server](https://github.com/jalateras/weather/tree/master) to fetch and process weather data using collaborative AI agents.

---

## Overview

**crewai-weather-mcp-agent** leverages the [CrewAI](https://crewai.com) platform to orchestrate multiple AI agents, each with specialized roles, for interacting with the weather MCP server. This project demonstrates how CrewAI agents can be integrated with external services to automate data retrieval and analysis workflows.

---

## Features

- Connects directly to the [weather MCP server](https://github.com/jalateras/weather/tree/master) for real-time weather data.
- Utilizes CrewAI's multi-agent framework for flexible, collaborative task execution.
- Easily customizable agent and task configurations.
- Designed for both local development and scalable deployment.

---

## Installation

**Prerequisites:**  
- Python >=3.10, <3.14  
- [UV](https://docs.astral.sh/uv/) for dependency management

**Install UV (if not already installed):**
First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

## Project Structure

- `src/my_ai_agent/config/agents.yaml` — Define agent roles and properties
- `src/my_ai_agent/config/tasks.yaml` — Specify tasks for the crew
- `src/my_ai_agent/crew.py` — Crew assembly and orchestration logic
- `src/my_ai_agent/main.py` — Project entry point
- `src/my_ai_agent/tools/custom_tool.py` — Integration with the weather MCP server

---

## Running the Project

Agents will connect to the weather MCP server and execute tasks as defined in your configuration files.

```bash
$ crewai run
```

This command initializes the my_ai_agent Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The my_ai_agent Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

- [CrewAI Documentation](https://docs.crewai.com)
- [CrewAI GitHub](https://github.com/joaomdmoura/crewai)
- [Join CrewAI Discord](https://discord.com/invite/X4JWnZnxPb)

For issues specific to the weather MCP server, see the [weather server repo](https://github.com/jalateras/weather/tree/master).


