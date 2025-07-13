from crewai import Crew
from agents import (
    research_agent, modeling_agent, report_agent,
    data_collection_agent, sentiment_analysis_agent,
    risk_assessment_agent, competitor_analysis_agent,
    esg_analyst_agent, macroeconomic_analyst_agent
)
from task import define_tasks

def run_crew(company_name: str):
    # Define all agents
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

    # Define the tasks using the company name
    tasks = define_tasks(company_name)

    # Initialize the Crew with all agents and tasks
    crew = Crew(
        agents=all_agents,
        tasks=tasks,
        verbose=True
    )

    # Run the crew and return results
    result = crew.kickoff()
    return result
