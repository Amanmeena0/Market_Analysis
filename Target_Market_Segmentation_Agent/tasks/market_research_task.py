"""
Market Research Task
===================

Primary market research task for industry analysis and competitive landscape research.
"""

from crewai import Task
from prompts import TaskOutputs


class MarketResearchTask:
    """
    Primary Market Research Task for comprehensive industry analysis.
    
    This task involves:
    - Industry reports and market sizing
    - Competitive landscape mapping
    - Market trends and growth analysis
    - Pricing and positioning research
    """
    
    @staticmethod
    def create_task(prompts: dict, market_researcher_agent):
        """
        Create the market research task.
        
        Args:
            prompts: Dictionary containing formatted prompts
            market_researcher_agent: The market researcher agent instance
            
        Returns:
            Configured CrewAI Task instance
        """
        return Task(
            description=prompts['market_research'],
            agent=market_researcher_agent,
            expected_output=TaskOutputs.MARKET_RESEARCH_OUTPUT
        )
