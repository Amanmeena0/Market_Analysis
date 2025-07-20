"""
Market Researcher Agent
======================

Primary market research agent responsible for industry analysis, market sizing,
and competitive landscape research using Google Search and web scraping tools.
"""

from crewai import Agent
from prompts import AgentBackstories, AgentRoles


class MarketResearcher:
    """
    Primary Market Research Agent for industry analysis and market intelligence.
    
    This agent specializes in:
    - Industry reports and market sizing
    - Competitive landscape analysis  
    - Market trends and growth patterns
    - Pricing and positioning research
    """
    
    @staticmethod
    def create_agent(llm, tools):
        """
        Create and configure the Market Researcher agent.
        
        Args:
            llm: The language model to use for this agent
            tools: List of tools to assign to this agent
            
        Returns:
            Configured CrewAI Agent instance
        """
        return Agent(
            role=AgentRoles.MARKET_RESEARCHER_ROLE,
            goal=AgentRoles.MARKET_RESEARCHER_GOAL,
            backstory=AgentBackstories.get_market_researcher_backstory(),
            tools=tools,
            llm=llm,
            verbose=True,
            allow_delegation=False
        )
