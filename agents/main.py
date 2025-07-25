from typing import List
from crewai.agent import BaseAgent
from .Barrier_Assessment.agent import *
from .Competetive_Analysis.agent import *
from .Market_Gap_Identification.agent import *
from .Industry_Research.agent import *
from .Sales_Forecast.agent import *
from .Target_Market_Segmentation.agent import *


agents: List[BaseAgent] = [
    industry_research_agent,
    competitive_analysis_agent,
    market_gap_agent,
    target_market_segmentation_agent,
    barrier_assessment_agent,
    sales_forecast_agent
]

tasks = [
    industry_research_task,
    competitive_analysis_task,
    market_gap_task,
    target_market_segmentation_task,
    barrier_assessment_task,
    sales_forecast_task
]

