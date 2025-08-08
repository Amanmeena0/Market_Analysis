from Industry_Research.agent import start_industry_research_agent
from Competetive_Analysis.agent import make_competitive_analysis_research_agent
from Sales_Forecast.agent import  make_sales_forecast_research_agent
from Market_Gap_Identification.agent import make_market_gap_research_agent
from Target_Market_Segmentation.agent import make_target_market_segmentation_research_agent
from Barrier_Assessment.agent import make_barrier_assessment_research_agent
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

async def main(user_prompt):
    client = MultiServerMCPClient(
                {
            "google_tools": {
                "url": "http://localhost:3000/mcp/google_mcp/sse",
                "transport": "sse",
            },
            "reddit_tools": {
                "url": "http://localhost:3000/mcp/reddit_mcp/sse",
                "transport": "sse",
            },
            "scraper_tools": {
                "url": "http://localhost:3000/mcp/scraper_mcp/sse",
                "transport": "sse",
            },
            "youtube_tools": {
                "url": "http://localhost:3000/mcp/youtube_mcp/sse",
                "transport": "sse",
            },
        }
    ) 

    tools = await client.get_tools()
    
    industry_research_report = await start_industry_research_agent(user_prompt, tools)
    # competitive_analysis_agent = await make_competitive_analysis_research_agent(user_prompt, tools)
    # market_gap_agent = await make_market_gap_research_agent(user_prompt, tools)
    # target_market_segmentation_agent = await make_target_market_segmentation_research_agent(user_prompt, tools)
    # barrier_assessment_agent = await make_barrier_assessment_research_agent(user_prompt, tools)
    # sales_forecast_agent = await make_sales_forecast_research_agent(user_prompt, tools)

    if isinstance(industry_research_report, str):
        with open("industry_research_report.md", "w",encoding='utf-8') as f:
            f.write(industry_research_report)



if __name__ == "__main__":
    import asyncio
    user_prompt = "Conduct market research on Beauty and Personal Care Market in India"
    asyncio.run(main(user_prompt))