from crewai import Agent, Crew, Process, Task
from crewai_tools import MCPServerAdapter
from llm import llm
from agents.main import agents,tasks

import mlflow

mlflow.crewai.autolog() # type: ignore

# Optional: Set a tracking URI and an experiment name if you have a tracking server
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("CrewAI")

server_params_list = [
    {"url": "http://localhost:3000/mcp/google_mcp/sse", "transport": "sse"},
    {"url": "http://localhost:3000/mcp/reddit_mcp/sse", "transport": "sse"},
    {"url": "http://localhost:3000/mcp/scraper_mcp/sse", "transport": "sse"},
    {"url": "http://localhost:3000/mcp/youtube_mcp/sse", "transport": "sse"},
]

try:
    with MCPServerAdapter(server_params_list) as aggregated_tools:  # type: ignore
        print(f"Available aggregated tools: {[tool.name for tool in aggregated_tools]}")

        for agent in agents:
            agent.tools = aggregated_tools
            agent.llm = llm 
        
        for i in range(1,len(tasks)):
            tasks[i].context = tasks[:i]

        crew = Crew(
            agents=agents,
            tasks=tasks,
            verbose=True,
            process=Process.sequential,
        )
        
        result = crew.kickoff()
        
        print(result)

except Exception as e:
    print(f"Error connecting to or using multiple MCP servers (Managed): {e}")
    print(
        "Ensure all MCP servers are running and accessible with correct configurations."
    )
