"""
Competitive Research Task
========================

Competitive intelligence task for analyzing competitors and market positioning.
"""

from crewai import Task
from prompts import TaskOutputs


class CompetitiveResearchTask:
    """
    Competitive Intelligence Research Task for competitor analysis.
    
    This task involves:
    - Competitor identification and analysis
    - Market positioning research
    - Competitive gap analysis
    - Pricing and feature comparison
    """
    
    @staticmethod
    def create_task(prompts: dict, competitive_analyst_agent):
        """
        Create the competitive research task.
        
        Args:
            prompts: Dictionary containing formatted prompts
            competitive_analyst_agent: The competitive analyst agent instance
            
        Returns:
            Configured CrewAI Task instance
        """
        return Task(
            description=prompts['competitive_research'],
            agent=competitive_analyst_agent,
            expected_output=TaskOutputs.COMPETITIVE_RESEARCH_OUTPUT
        )
