from crewai.tools import tool
import requests
import yfinance as yf
import os
import logging
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
serper_api_key = os.environ.get("SERPER_API_KEY")

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@tool("CompanyProfileTool")
def get_company_profile(company_name: str) -> str:
    """Fetch a quick company profile using Yahoo Finance."""
    try:
        ticker = yf.Ticker(company_name)
        info = ticker.info
        profile = (
            f"Name: {info.get('longName', 'N/A')}, "
            f"Sector: {info.get('sector', 'N/A')}, "
            f"Industry: {info.get('industry', 'N/A')}, "
            f"Market Cap: {info.get('marketCap', 'N/A')}"
        )
        logger.info(f"Fetched company profile for: {company_name}")
        return profile
    except Exception as e:
        logger.error(f"Error in get_company_profile: {str(e)}")
        return f"Error fetching profile for {company_name}"

@tool("LatestNewsTool")
def get_latest_news(company_name: str) -> str:
    """Fetch latest news articles using Serper API."""
    url = "https://google.serper.dev/news"
    payload = json.dumps({"q": company_name})
    headers = {
        "X-API-KEY": serper_api_key,
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        articles = response.json().get("news", [])
        if not articles:
            return "No recent news found."

        news_summary = "\n".join([f"- {article['title']}: {article['link']}" for article in articles[:5]])
        logger.info(f"Fetched news for: {company_name}")
        with open("news_log.txt", "w") as log_file:
            log_file.write(f"{company_name} News:\n{news_summary}\n\n")
    except Exception as e:
        logger.error(f"Error in get_latest_news: {str(e)}")
        return f"News fetch failed for {company_name}."


@tool("DataCollectionTool")
def collect_data_sources(topic: str) -> str:
    """Collect structured/unstructured data related to a topic."""
    logger.info(f"Collecting data sources for: {topic}")
    return f"Stub: Collected structured data for topic '{topic}' from multiple sources."

@tool("SentimentAnalysisTool")
def sentiment_analysis(text: str) -> str:
    """Analyze sentiment of the given text."""
    logger.info("Performing sentiment analysis")
    if "loss" in text or "fall" in text:
        return "Negative sentiment detected."
    elif "growth" in text or "profit" in text:
        return "Positive sentiment detected."
    return "Neutral sentiment."

@tool("RiskAssessmentTool")
def assess_risks(company_name: str) -> str:
    """Provide a general risk assessment of the company."""
    logger.info(f"Assessing risk for: {company_name}")
    return f"Risks for {company_name}: Market volatility, regulatory challenges, cyber risks."

@tool("CompetitorAnalysisTool")
def analyze_competitors(company_name: str) -> str:
    """Benchmark a company with competitors."""
    logger.info(f"Analyzing competitors for: {company_name}")
    return f"{company_name} is compared to ABC Corp and DEF Inc. Strength: Pricing. Weakness: Innovation."

@tool("ESGFetcherTool")
def esg_data_fetcher(company_name: str) -> str:
    """Evaluate ESG (Environmental, Social, Governance) performance."""
    logger.info(f"Fetching ESG data for: {company_name}")
    return f"{company_name} ESG Scores – Environmental: 76, Social: 84, Governance: 70"

@tool("MacroeconomicDataTool")
def macroeconomic_data(region: str) -> str:
    """Provide macroeconomic indicators for a region."""
    logger.info(f"Fetching macroeconomic data for: {region}")
    return f"{region} Indicators – GDP Growth: 5.4%, Inflation: 4.8%, Unemployment: 6.3%"
