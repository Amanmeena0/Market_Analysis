from ..utils import *
from ..state import *
from ..graph import make_graph
from prompt import *
from typing import List
from langchain_core.tools import BaseTool

async def make_market_gap_research_agent(tools: List[BaseTool]):

    market_gap_agent = await make_graph(
        tools=tools,
        reflection_instructions_prompt=reflection_instructions_prompt,
        fill_gaps_prompt=fill_gaps_prompt,
        merge_gaps_prompt=merge_gaps_prompt
    ) 

    return market_gap_agent

