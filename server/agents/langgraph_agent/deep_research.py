# from typing import List
# from langchain_mcp_adapters.client import MultiServerMCPClient
# from langchain_core.messages import HumanMessage, AIMessage
# from langchain_core.language_models import BaseChatModel
# from langgraph.graph import StateGraph, END, MessagesState
# from langgraph.prebuilt import create_react_agent
# from langchain_core.prompts import PromptTemplate
# from dotenv import load_dotenv
# from langgraph.prebuilt import ToolNode
# import asyncio
# from ..utils import *

# load_dotenv()


# client = MultiServerMCPClient(
#     {
#         "google_tools": {
#             "url": "http://localhost:3000/mcp/google_mcp/sse",
#             "transport": "sse",
#         },
#         "reddit_tools": {
#             "url": "http://localhost:3000/mcp/reddit_mcp/sse",
#             "transport": "sse",
#         },
#         "scraper_tools": {
#             "url": "http://localhost:3000/mcp/scraper_mcp/sse",
#             "transport": "sse",
#         },
#         "youtube_tools": {
#             "url": "http://localhost:3000/mcp/youtube_mcp/sse",
#             "transport": "sse",
#         },
#     }
# )


# class AgentState(MessagesState):
#     knowledge_gaps:str 
#     filled_gaps:str
#     k : int 

# async def industry_research(system_prompt: str,user_prompt:str, llm: BaseChatModel,tools:List[BaseTool]):

#     tools = await client.get_tools()
#     tool_llm = llm.bind_tools(tools)
#     tool_node = ToolNode(tools)

#     def find_gaps(state:AgentState):
#         last_message = state["messages"][-1]
#         rf_prompt = reflection_instructions_prompt.invoke({'report': last_message.content})  

#         response = call_llm_with_backoff(llm, [HumanMessage(content=rf_prompt.to_string())]) 

#         return {"knowledge_gaps": response.content if response else ""}
    
#     def fill_gaps(state:AgentState):
#         gaps = state["knowledge_gaps"]

#         if not gaps:
#             return {"filled_gaps": "", "messages": []}
        
#         fill_prompt = fill_gaps_prompt.invoke({'gaps': gaps})
#         response = call_tool_llm_with_backoff(tool_llm, [HumanMessage(content=fill_prompt.to_string())])

#         # If there are tool calls, we need to pass the message to the graph for tool execution
#         if isinstance(response, AIMessage) and response.tool_calls:
#             return {"messages": [response], "filled_gaps": ""}
#         else:
#             return {"filled_gaps": response.content if response else "", "messages": []}

#     def merge_filled_gaps(state:AgentState):
#         filled_gaps = state["filled_gaps"]
#         report = state["messages"][-1].content
        
#         merge_prompt = merge_gaps_prompt.invoke({'report': report, 'filled_gaps': filled_gaps})
        
#         response = call_llm_with_backoff(llm, [HumanMessage(content=merge_prompt.to_string())])
        
#         return {"messages": [HumanMessage(content=response.content if response else "")],"k": state["k"] + 1}

#     def route_tools(state: AgentState) :
#         """After agent_step or fill_gaps, decide to run tools or continue."""
#         # Check if there are any new messages with tool calls
#         if state.get("messages") and len(state["messages"]) > 0:
#             last = state["messages"][-1]
#             # Only AIMessage can have tool_calls
#             if isinstance(last, AIMessage) and last.tool_calls:
#                 return "tools"
#         return "merge_filled_gaps"

#     def route_loop(state: AgentState):
#         """After merge_filled_gaps decide to iterate or finish."""
#         return "find_gaps" if state["k"] < 5 else "final"

#     def final_node(state: AgentState):
#         """Final node to return the final report."""
#         last_message = state["messages"][-1]
#         return {"messages": [HumanMessage(content=last_message.content)]}

#     # 5.  Build the graph
#     workflow = StateGraph(AgentState)
#     workflow.add_node("find_gaps", find_gaps)
#     workflow.add_node("fill_gaps", fill_gaps)
#     workflow.add_node("tools", tool_node)
#     workflow.add_node("merge_filled_gaps", merge_filled_gaps)
#     workflow.add_node("final", final_node)

#     workflow.set_entry_point("find_gaps")  # Start with finding gaps

#     workflow.add_edge("find_gaps","fill_gaps")
#     workflow.add_conditional_edges("fill_gaps",route_tools, ["tools", "merge_filled_gaps"])
#     workflow.add_edge("tools", "merge_filled_gaps")
#     workflow.add_conditional_edges("merge_filled_gaps", route_loop, ["find_gaps", "final"])
#     workflow.add_edge("final", END)
        
    
#     graph = workflow.compile()

#     react_agent = create_react_agent(
#         model=llm,
#         tools=tools,
#         prompt=system_prompt
#     )

#     report = await react_agent.ainvoke({
#         'messages': [
#             {'role':'user', 'content': user_prompt},
#         ]
#     })

#     report = report['messages'][-1]  # type: ignore

#     print("Initial Report Generated:\n", report.content)  # type: ignore

#     async for message, metadata in graph.astream(
#         {
#             "messages": [HumanMessage(content=report.content)],  # type: ignore
#             'filled_gaps': "",
#             'knowledge_gaps': "",
#             'k': 0,
#         }, # type: ignore
#         stream_mode="messages",
#     ):  # type: ignore
#         if message:
#             print(f"Node: {metadata['langgraph_node']} \n Message: {message.content}")  # type: ignore


# if __name__ == "__main__":
#     import asyncio

#     user_prompt = "Conduct a comprehensive industry analysis on EV Sector in India"

#     asyncio.run(industry_research(PROMPT, user_prompt, llm))
