"""
Tasks Module for Target Market Segmentation
===========================================

This module contains all the CrewAI tasks used in the market segmentation research process.
Each task represents a specific research activity performed by the agents.
"""

from .market_research_task import MarketResearchTask
from .social_research_task import SocialResearchTask
from .competitive_research_task import CompetitiveResearchTask
from .segmentation_synthesis_task import SegmentationSynthesisTask

__all__ = [
    'MarketResearchTask',
    'SocialResearchTask',
    'CompetitiveResearchTask', 
    'SegmentationSynthesisTask'
]
