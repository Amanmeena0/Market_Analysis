"""
Competitive Intelligence Analyst
===============================

Competitive analysis agent responsible for analyzing competitors,
market positioning, and identifying competitive gaps and opportunities.
"""

from crewai import Agent
from prompts import AgentBackstories, AgentRoles
from tools import GOOGLE_TOOLS


class CompetitiveAnalyst:
    """
    Competitive Intelligence Agent for competitor analysis and market positioning.
    
    This agent specializes in:
    - Competitor identification and analysis
    - Market positioning research
    - Competitive gap analysis
    - Pricing and feature comparison
    """
    
    @staticmethod
    def create_agent(llm, tools):
        """
        Create and configure the Competitive Analyst agent.
        
        Args:
            llm: The language model to use for this agent
            tools: List of tools to assign to this agent
            
        Returns:
            Configured CrewAI Agent instance
        """
        return Agent(
            role=AgentRoles.COMPETITIVE_ANALYST_ROLE,
            goal=AgentRoles.COMPETITIVE_ANALYST_GOAL,
            backstory=AgentBackstories.get_competitive_analyst_backstory(),
            tools=tools,
            llm=llm,
            verbose=True,
            allow_delegation=False
        )
