from typing import List
from langchain_core.tools import BaseTool
from langchain_core.messages import ToolMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import  AIMessageChunk
from ..utils import *
from ..state import *
from ..graph import make_graph
from .prompt import *


async def start_industry_research_agent(user_prompt: str, tools: List[BaseTool]):

    llm = get_llm()

    industry_research_agent = await make_graph(
        tools=tools,
        reflection_instructions_prompt=reflection_instructions_prompt,
        fill_gaps_prompt=fill_gaps_prompt,
        merge_gaps_prompt=merge_gaps_prompt,
    )

    print("Starting Industry Research Agent...")
    print("Making initial Report...")

    react_agent = create_react_agent(model=llm, tools=tools, prompt=PROMPT)

    report = react_agent.astream(
        {
            "messages": [
                {"role": "user", "content": user_prompt},
            ],
        },
        stream_mode="values",
    )

    init_report = ""

    async for message in report:
        last_message = message["messages"][-1]  # type: ignore
        if isinstance(last_message, ToolMessage):
            print(f"Results:\n {last_message.content}")
        elif isinstance(last_message, AIMessage):
            print(f"{last_message.content}", sep="", flush=True)  # type: ignore
            for tool_call in last_message.tool_calls:
                print(f"Tool Call:\n {tool_call['name']}")
                print(f"Arguments:\n {tool_call['args']}")

            init_report = last_message.content  # type: ignore

    print("Thinking...")
    currentNode = None

    async for stream_mode, message in industry_research_agent.astream(
        {
            "knowledge_gaps": "",
            "filled_gaps": "",
            "k": 0,
            "report": init_report,  # type: ignore
        }, # type: ignore
        stream_mode=["updates", "messages","custom"],
    ):
        if stream_mode == "updates":
            if "final" in message:
                final_report = message["final"]["report"]  # type: ignore

            if "merge_filled_gaps" in message:
                print("=" * 30, f"REPORT: {message['merge_filled_gaps']['report']}", "=" * 30)  # type: ignore
                print("=" * 30, f"ITERATION:{message['merge_filled_gaps']['k']}", "=" * 30)  # type: ignore
        else:
            if 'react_agent' in message:
                msg = message['react_agent']['messages'][-1] # type: ignore
                
                if isinstance(msg, AIMessageChunk) or isinstance(msg, AIMessage):
                    print(msg.content, end="", flush=True)
                elif isinstance(msg,ToolMessage):
                    print(f"Tool Call: {msg.name}")
                    print(msg.content, end="", flush=True)
            else:
                message_chunk = message[0]
                metadata = message[1]
                if currentNode != metadata["langgraph_node"]:  # type: ignore
                    currentNode = metadata["langgraph_node"]  # type: ignore
                    print(f"\nNode: {currentNode}\n")

                if currentNode == "tools":
                    print(f"Tool Call:")  # type: ignore
                    print(message_chunk.content, sep="", flush=True)  # type: ignore
                if currentNode == "find_gaps" or currentNode == "fill_gaps":
                    print(f"{message_chunk.content}", sep="", flush=True)  # type: ignore
                
                 
                
    return final_report

