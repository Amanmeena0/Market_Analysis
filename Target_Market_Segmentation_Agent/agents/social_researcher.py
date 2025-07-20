"""
Social Media Researcher Agent
============================

Social media and community research agent responsible for analyzing 
YouTube content, Reddit discussions, and social sentiment analysis.
"""

from crewai import Agent
from prompts import AgentBackstories, AgentRoles


class SocialResearcher:
    """
    Social Media & Community Research Agent for social intelligence gathering.
    
    This agent specializes in:
    - YouTube video content analysis
    - Reddit community discussions
    - Social media sentiment analysis
    - User feedback and review analysis
    """
    
    @staticmethod
    def create_agent(llm, tools):
        """
        Create and configure the Social Researcher agent.
        
        Args:
            llm: The language model to use for this agent
            tools: List of tools to assign to this agent
            
        Returns:
            Configured CrewAI Agent instance
        """
        return Agent(
            role=AgentRoles.SOCIAL_RESEARCHER_ROLE,
            goal=AgentRoles.SOCIAL_RESEARCHER_GOAL,
            backstory=AgentBackstories.get_social_researcher_backstory(),
            tools=tools,
            llm=llm,
            verbose=True,
            allow_delegation=False
        )
