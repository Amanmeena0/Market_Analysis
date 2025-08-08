# from langchain_mcp_adapters.client import MultiServerMCPClient
# from langgraph.prebuilt import create_react_agent
# import asyncio
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.prompts import PromptTemplate

# from langchain_core.rate_limiters import InMemoryRateLimiter

# rate_limiter = InMemoryRateLimiter(
#     requests_per_second=0.25,  # <-- Super slow! We can only make a request once every 4 seconds!!
#     check_every_n_seconds=0.1,  # Wake up every 100 ms to check whether allowed to make a request,
#     max_bucket_size=10,  # Controls the maximum burst size.
# )

# load_dotenv()

# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash",
#     rate_limiter=rate_limiter,
# )

# # template = """Answer the following questions as best you can. You have access to the following tools:

# # {tools}

# # Use the following format:

# # Question: the input question you must answer
# # Thought: you should always think about what to do
# # Action: the action to take, should be one of [{tool_names}]
# # Action Input: the input to the action
# # Observation: the result of the action
# # ... (this Thought/Action/Action Input/Observation can repeat N times)
# # Thought: I now know the final answer
# # Final Answer: the final answer to the original input question

# # Begin!

# # Question: {input}
# # Thought:{agent_scratchpad}"""

# # prompt = PromptTemplate.from_template(template)
# from langchain_core.messages import HumanMessage


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

# # SYSTEM_MESSAGE = (
# #     "You are a senior market-research analyst. "
# #     "Use the provided tools to gather all required information, "
# #     "then synthesize a concise report."
# # )


# async def main():
#     tools = await client.get_tools()
#     agent = create_react_agent(
#         model=llm,
#         tools=tools,
#         prompt="You are an experienced market research analyst with deep expertise in industry analysis, competitive intelligence, and market trend identification. You excel at gathering and synthesizing data from multiple sources. You specialize in scraping and regrouping industry statistics such as market size, number of businesses, revenue, and external factors including laws, technology trends, and socio-economic indicators to provide actionable insights for business decision-making. All your answers should be based on any of the tools' results.DON'T ASSUME ANYTHING.Keep repeating this process until all the information is gathered.\nExpected output: A DETAILED AND COMPREHENSIVE industry analysis report including: market size and growth projections, competitive landscape overview, key industry players and their market share, regulatory and legal considerations, technological trends affecting the industry, economic factors and market opportunities, potential risks and challenges, and actionable recommendations for market entry or expansion strategies.\nReturn your final answer as a well-structured Markdown report. Each section should contain complete and relevant data and insights gathered from the tools. If you cannot find any information, state that clearly in the report.\n\nYou must use the tools provided to gather information. Do not make assumptions or provide information that is not based on the tools' results. ADD CITATIONS TO THE REPORT FOR EACH TOOL USED AND SOURCE LINKS.",
#     )
    
#     final_answer = None

#     # Collect events as they happen
#     # async for event in agent.astream_events(
#     #     {
#     #         "messages": [
#     #             HumanMessage(
#     #                 content="Conduct a comprehensive industry analysis on EV Sector in India"
#     #             )
#     #         ]
#     #     },
#     #     version="v1",
#     # ):
#     #     kind = event["event"]
#     #     data = event["data"]

#     #     # 1. LLM is "thinking" (generating a reasoning block)
#     #     if kind == "on_chat_model_stream":
#     #         chunk = data.get("chunk")
#     #         if chunk and chunk.content:
#     #             print(chunk.content, end="", flush=True)  # streaming tokens

#     #     # 2. Tool is about to be called
#     #     elif kind == "on_tool_start":
#     #         print("\n--- TOOL CALL ---")
#     #         print("Tool:", event["name"])
#     #         print("Args:", event["data"].get("input"))

#     #     # 3. Tool finished and returned something
#     #     elif kind == "on_tool_end":
#     #         print("\n--- TOOL RESULT ---")
#     #         print("Tool:", event["name"])
#     #         print("Output:", data.get("output"))

#     #     # 4. Final message from the agent
#     #     elif kind == "on_chain_end" and "messages" in data:
#     #         last_msg = data["messages"][-1]
#     #         if last_msg.type == "ai":
#     #             print("\n--- FINAL ANSWER ---")
#     #             print(last_msg.content)
#     #             final_answer = last_msg.content

#     # if final_answer:
#     #     with open("industry_analysis_report.md", "w", encoding='utf-8') as f:
#     #         f.write(final_answer)
#     #         print('written to file')

#     result = agent.astream({
#         "messages": [
#             HumanMessage(
#                 content="Conduct a comprehensive industry analysis on EV Sector in India"
#             )
#         ]
#     },stream_mode='messages')

    
#     async for message_chunk, metatdata in result:
#         if message_chunk:
#             print(message_chunk.content, end="", flush=True) # type: ignore


# if __name__ == "__main__":
#     asyncio.run(main())
