from typing import List
from langchain_core.tools import BaseTool
from ..utils import *
from ..state import *
from ..graph import make_graph
from prompt import *


async def make_sales_forecast_research_agent(tools: List[BaseTool]):
    sales_forecast_agent = await make_graph(
        tools=tools,
        reflection_instructions_prompt=reflection_instructions_prompt,
        fill_gaps_prompt=fill_gaps_prompt,
        merge_gaps_prompt=merge_gaps_prompt
    ) 

    return sales_forecast_agent



