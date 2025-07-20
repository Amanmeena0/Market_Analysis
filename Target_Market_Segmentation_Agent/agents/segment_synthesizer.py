"""
Market Segmentation Synthesizer
==============================

Synthesis agent responsible for combining research findings from all other agents
and creating comprehensive market segments with strategic recommendations.
"""

from crewai import Agent
from prompts import AgentBackstories, AgentRoles


class SegmentSynthesizer:
    """
    Market Segmentation Synthesizer Agent for strategic synthesis and segment creation.
    
    This agent specializes in:
    - Synthesizing multi-source research findings
    - Creating comprehensive market segments
    - Developing strategic recommendations
    - Identifying market opportunities and priorities
    """
    
    @staticmethod
    def create_agent(llm, tools=None):
        """
        Create and configure the Segment Synthesizer agent.
        
        Args:
            llm: The language model to use for this agent
            tools: List of tools (typically empty for synthesis agent)
            
        Returns:
            Configured CrewAI Agent instance
        """
        return Agent(
            role=AgentRoles.SEGMENT_SYNTHESIZER_ROLE,
            goal=AgentRoles.SEGMENT_SYNTHESIZER_GOAL,
            backstory=AgentBackstories.get_segment_synthesizer_backstory(),
            tools=tools or [],  # This agent primarily synthesizes findings from other agents
            llm=llm,
            verbose=True,
            allow_delegation=False
        )
