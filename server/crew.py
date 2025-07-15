import os
from dotenv import load_dotenv
from crewai import Crew
from langchain_google_genai import ChatGoogleGenerativeAI
# Load API keys from .env

from agents import (
    research_agent, modeling_agent, report_agent,
    data_collection_agent, sentiment_analysis_agent,
    risk_assessment_agent, competitor_analysis_agent,
    esg_analyst_agent, macroeconomic_analyst_agent
)
from task import define_tasks


load_dotenv()


def run_crew(company_name: str):
    # Step 1: Initialize the LLM
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.environ.get("GOOGLE_API_KEY"),
        temperature=0.5,
        verbose=True
    )

    # Step 2: Define all agents
    all_agents = [
        data_collection_agent,
        research_agent,
        sentiment_analysis_agent,
        risk_assessment_agent,
        competitor_analysis_agent,
        esg_analyst_agent,
        macroeconomic_analyst_agent,
        modeling_agent,
        report_agent
    ]

    # Step 3: Define the tasks using the company name
    tasks = define_tasks(company_name)

    # Step 4: Initialize the Crew with all agents, tasks, and LLM
    crew = Crew(
        agents=all_agents,
        tasks=tasks,
        llm=llm,            # 🔥 CRITICAL: Add this line
        verbose=True
    )

    # Step 5: Run the crew and return results
    result = crew.kickoff()
    return result
