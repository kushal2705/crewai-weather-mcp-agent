from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import MCPServerAdapter
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from huggingface_hub import InferenceClient
import os

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class MyAiAgent():
    """MyAiAgent crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        super().__init__()
        # Configure MCP server connection for streamable-http transport
        self.server_params = {
            "url": os.getenv("MCP_SERVER_URL", "http://localhost:9000/mcp/"),
            "transport": "streamable-http",
            "timeout": 60,
            "headers": {"Content-Type": "application/json"},
        }
        self.llm_client = InferenceClient(
            provider="novita",
            api_key=os.getenv("HF_API_KEY")  # Store key in .env
        )
        # LiteLLM configuration for Hugging Face
        self.hf_llm = LLM(
            model="huggingface/meta-llama/Llama-3.1-8B-Instruct",  # Prefix with huggingface/
            api_key=os.getenv("HF_API_KEY"),     # Use standard env var name
            temperature=0.7,
            max_tokens=1000
        )

    def _get_mcp_tools_and_print(self):
        """Get MCP tools using MCPServerAdapter and print available tools"""
        try:
            with MCPServerAdapter(self.server_params) as tools:
                print(f"✅ Successfully connected to MCP server: {self.server_params['url']}")
                print(f"🔧 Available MCP tools: {len(tools)} tools found")
                print("-" * 50)

                for i, tool in enumerate(tools, 1):
                    print(f"{i}. {tool.name}")
                    if hasattr(tool, 'description') and tool.description:
                        print(f"   Description: {tool.description}")
                    if hasattr(tool, 'parameters') and tool.parameters:
                        print(f"   Parameters: {tool.parameters}")
                    print()

                print("-" * 50)
                return tools

        except Exception as e:
            print(f"❌ Failed to connect to MCP server: {e}")
            print(f"   Server URL: {self.server_params['url']}")
            print(f"   Transport: {self.server_params['transport']}")
            return []

    def _get_mcp_tools(self):
        """Get MCP tools using MCPServerAdapter"""
        return MCPServerAdapter(self.server_params)

    def _hf_llm(self, messages, **kwargs):
        """Custom LLM handler for Novita provider"""
        completion = self.llm_client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",  # Your working model
            messages=messages,
            **kwargs
        )
        return completion.choices[0].message.content

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools

   # @agent
   # def weather_agent(self) -> Agent:
   #     """Weather forecasting specialist with MCP weather tools"""
   #     # Print available tools when creating the agent
   #     print("\n🤖 Initializing Weather Agent...")
   #     tools = self._get_mcp_tools_and_print()
   #     return Agent(
   #         config=self.agents_config['weather_agent'],
   #         tools=self._get_mcp_tools(),  # Inject MCP weather tools
   #         verbose=True
   #     )
    
    @agent
    def weather_agent(self) -> Agent:
      print("\n🤖 Initializing Weather Agent...")
      adapter = MCPServerAdapter(self.server_params)
      try:
        # Get the actual list of Tool objects
        tools = adapter.tools
        print(f"✅ Connected to MCP server: found {len(tools)} tools")
        for t in tools:
            print(f" - {t.name}")
      except Exception as e:
        print(f"❌ MCP connect failed: {e}")
        # Fallback to no tools if the connection or discovery fails
        tools = []

      # Create CrewAI agent with HF LLM
      return Agent(
        config=self.agents_config['weather_agent'],
        #llm=self._hf_llm,  # Custom LLM handler
        llm=self.hf_llm,
        tools=tools,
        verbose=True,
      )

    @agent
    def analyst_agent(self) -> Agent:
        """Weather data analyst for insights and recommendations"""
        return Agent(
            config=self.agents_config['analyst_agent'],
            #llm=self._hf_llm,  # Custom LLM handler
            llm=self.hf_llm,
            verbose=True,
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def weather_forecast_task(self) -> Task:
        """Task to retrieve weather forecast using MCP tools"""
        return Task(
            config=self.tasks_config['weather_forecast_task'],
        )

    @task
    def analysis_task(self) -> Task:
        """Task to analyze weather data and provide recommendations"""
        return Task(
            config=self.tasks_config['analysis_task'],
            output_file='weather_analysis.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Weather AI crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            #manager_llm=self._hf_llm,            # ← override default orchestration LLM
            #function_calling_llm=self._hf_llm
            manager_llm=self.hf_llm,
            function_calling_llm=self.hf_llm
        )
