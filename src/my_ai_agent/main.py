#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime
from dotenv import load_dotenv

from my_ai_agent.crew import MyAiAgent

# Load environment variables for MCP server configuration
load_dotenv()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the weather AI crew.
    """
    # Weather-specific inputs for San Francisco as example
    inputs = {
        'latitude': 37.7749,
        'longitude': -122.4194,
        'location_name': 'San Francisco, CA',
        'forecast_days': 3,
        'state': 'CA',  # For weather alerts
        'current_date': datetime.now().strftime('%Y-%m-%d')
    }
    
    print("🌤️  Starting Weather AI Agent Crew...")
    print(f"📍 Location: {inputs['location_name']}")
    print(f"📊 Forecast Days: {inputs['forecast_days']}")
    print(f"🚨 Checking alerts for: {inputs['state']}")
    print("-" * 50)
    
    try:
        result = MyAiAgent().crew().kickoff(inputs=inputs)
        print("\n" + "="*60)
        print("🎯 WEATHER ANALYSIS COMPLETE")
        print("="*60)
        print(result)
        return result
    except Exception as e:
        print(f"❌ Error occurred while running the weather crew: {e}")
        print(f"🔧 Make sure your MCP server is running at: {os.getenv('MCP_SERVER_URL', 'http://localhost:9000/mcp/')}")
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'latitude': 37.7749,
        'longitude': -122.4194,
        'location_name': 'San Francisco, CA',
        'forecast_days': 3,
        'state': 'CA',
        'current_date': datetime.now().strftime('%Y-%m-%d')
    }
    
    try:
        MyAiAgent().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        MyAiAgent().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'latitude': 37.7749,
        'longitude': -122.4194,
        'location_name': 'San Francisco, CA',
        'forecast_days': 3,
        'state': 'CA',
        'current_date': datetime.now().strftime('%Y-%m-%d')
    }
    
    try:
        MyAiAgent().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def check_mcp_connection():
    """
    Check if MCP server is accessible before running the crew.
    """
    from crewai_tools import MCPServerAdapter
    
    server_params = {
        "url": os.getenv("MCP_SERVER_URL", "http://localhost:9000/mcp/"),
        "transport": "streamable-http"
    }
    
    print(f"🔍 Checking MCP server connection at: {server_params['url']}")
    
    try:
        with MCPServerAdapter(server_params) as tools:
            print(f"✅ MCP server connected successfully!")
            print(f"🔧 Available tools: {[tool.name for tool in tools]}")
            return True
    except Exception as e:
        print(f"❌ Failed to connect to MCP server: {e}")
        print(f"   Make sure your weather MCP server is running")
        print(f"   Server URL: {server_params['url']}")
        return False

if __name__ == "__main__":
    # Check MCP connection before running
    if len(sys.argv) == 1:  # Default run
        if check_mcp_connection():
            run()
        else:
            print("🛑 Cannot proceed without MCP server connection")
    else:
        # Handle other commands (train, test, replay)
        command = sys.argv[0].split('/')[-1] if '/' in sys.argv[0] else 'main.py'
        print(f"Running {command} with arguments: {sys.argv[1:]}")
