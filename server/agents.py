from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import (
    get_company_profile, 
    get_latest_news, 
    collect_data_sources, 
    sentiment_analysis, 
    assess_risks, 
    analyze_competitors, 
    esg_data_fetcher, 
    macroeconomic_data
)
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.environ.get("GOOGLE_API_KEY"),
    temperature=0.5,
    verbose=True
)

def format_datasets(datasets):
    formatted_output = ""
    for dataset in datasets:
        title = dataset.get("title", "Unknown Title")
        description = dataset.get("description", "No description available.")
        links = dataset.get("links", [])
        formatted_output += f"{title}\t{description}\t" + "\n".join(links) + "\n\n"
    return formatted_output

# Core Agents
research_agent = Agent(
    role="Market Research Analyst",
    goal="Collect detailed financial and market data for the company",
    backstory="Expert in market analysis, financials, and research sourcing",
    tools=[get_company_profile, get_latest_news],
    verbose=True,
    memory=True,
    allow_delegation=True,
    llm=llm
)

modeling_agent = Agent(
    role="Financial Modeler",
    goal="Analyze financial data and predict market trends",
    backstory="Expert in DCF, valuation metrics, and forecasting",
    tools=[get_latest_news],
    verbose=True,
    memory=True,
    allow_delegation=True,
    llm=llm
)

report_agent = Agent(
    role="Financial Report Writer",
    goal="Compile research into a well-structured, executive-level summary",
    backstory="Finance writer skilled in transforming analysis into insights",
    tools=[get_latest_news],
    verbose=True,
    memory=True,
    allow_delegation=True,
    llm=llm
)
# Specialized Agents for Advanced Analysis
# 1. Data Collection Agent
data_collection_agent = Agent(
    role="Data Collection Specialist",
    goal="Gather structured and unstructured data from a variety of trusted sources",
    backstory="Expert in scraping, APIs, and structured data extraction",
    tools=[collect_data_sources],
    verbose=True,
    memory=True,
    allow_delegation=False,
    llm=llm
)

# 2. Sentiment Analysis Agent
sentiment_analysis_agent = Agent(
    role="Sentiment Analyst",
    goal="Perform sentiment analysis on news, reports, and market chatter",
    backstory="Data scientist with experience in NLP and public sentiment trends",
    tools=[sentiment_analysis],
    verbose=True,
    memory=True,
    allow_delegation=False,
    llm=llm
)

# 3. Risk Assessment Agent
risk_assessment_agent = Agent(
    role="Risk Assessment Officer",
    goal="Identify and quantify potential financial, operational, and geopolitical risks",
    backstory="Risk analyst with deep expertise in market vulnerabilities and modeling",
    tools=[assess_risks],
    verbose=True,
    memory=True,
    allow_delegation=False,
    llm=llm
)

# 4. Competitor Analysis Agent
competitor_analysis_agent = Agent(
    role="Competitor Analyst",
    goal="Benchmark the company against key competitors across financial and strategic metrics",
    backstory="Industry analyst with access to competitive intelligence databases",
    tools=[analyze_competitors],
    verbose=True,
    memory=True,
    allow_delegation=False,
    llm=llm
)

# 5. ESG Analyst Agent
esg_analyst_agent = Agent(
    role="ESG Analyst",
    goal="Evaluate the company’s environmental, social, and governance performance",
    backstory="Sustainability expert with knowledge of ESG frameworks and global standards",
    tools=[esg_data_fetcher],
    verbose=True,
    memory=True,
    allow_delegation=False,
    llm=llm
)

# 6. Macroeconomic Analyst Agent
macroeconomic_analyst_agent = Agent(
    role="Macroeconomic Analyst",
    goal="Assess macroeconomic indicators that could impact the company or industry",
    backstory="Economist with a deep understanding of inflation, interest rates, and global trends",
    tools=[macroeconomic_data],
    verbose=True,
    memory=True,
    allow_delegation=False,
    llm=llm
)
