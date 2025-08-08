from typing import List
from langchain_core.tools import BaseTool
from ..utils import *
from ..state import *
from ..graph import make_graph
from prompt import *


async def make_barrier_assessment_research_agent(tools: List[BaseTool]):

    barrier_assessment_agent = await make_graph(
        tools=tools,
        reflection_instructions_prompt=reflection_instructions_prompt,
        fill_gaps_prompt=fill_gaps_prompt,
        merge_gaps_prompt=merge_gaps_prompt
    ) 

    return barrier_assessment_agent


