"""
Social Media Research Task
=========================

Social media and community research task for analyzing user sentiment and behavior.
"""

from crewai import Task
from prompts import TaskOutputs


class SocialResearchTask:
    """
    Social Media & Community Research Task for social intelligence gathering.
    
    This task involves:
    - YouTube video content analysis
    - Reddit community discussions
    - Social media sentiment analysis
    - User feedback and review analysis
    """
    
    @staticmethod
    def create_task(prompts: dict, social_researcher_agent):
        """
        Create the social research task.
        
        Args:
            prompts: Dictionary containing formatted prompts
            social_researcher_agent: The social researcher agent instance
            
        Returns:
            Configured CrewAI Task instance
        """
        return Task(
            description=prompts['social_research'],
            agent=social_researcher_agent,
            expected_output=TaskOutputs.SOCIAL_RESEARCH_OUTPUT
        )
