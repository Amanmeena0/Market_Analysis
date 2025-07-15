from crewai.tools import tool
import requests
import yfinance as yf
import os
import logging
import json
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Dict, List, Any
import pandas as pd
from textblob import TextBlob
import re

# Load environment variables
load_dotenv()
serper_api_key = os.environ.get("SERPER_API_KEY")
alpha_vantage_api_key = os.environ.get("ALPHA_VANTAGE_API_KEY")

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@tool("CompanyProfileTool")
def get_company_profile(company_name: str) -> str:
    """Fetch comprehensive company profile using Yahoo Finance."""
    try:
        ticker = yf.Ticker(company_name)
        info = ticker.info
        
        # Get additional financial metrics
        market_cap = info.get('marketCap', 'N/A')
        if market_cap != 'N/A' and isinstance(market_cap, (int, float)):
            market_cap = f"${market_cap:,.0f}"
        
        revenue = info.get('totalRevenue', 'N/A')
        if revenue != 'N/A' and isinstance(revenue, (int, float)):
            revenue = f"${revenue:,.0f}"
        
        employees = info.get('fullTimeEmployees', 'N/A')
        if employees != 'N/A':
            employees = f"{employees:,}"
        
        profile = {
            "company_name": info.get('longName', 'N/A'),
            "symbol": info.get('symbol', company_name),
            "sector": info.get('sector', 'N/A'),
            "industry": info.get('industry', 'N/A'),
            "market_cap": market_cap,
            "revenue": revenue,
            "employees": employees,
            "headquarters": f"{info.get('city', 'N/A')}, {info.get('country', 'N/A')}",
            "website": info.get('website', 'N/A'),
            "business_summary": info.get('businessSummary', 'N/A')[:200] + "..." if info.get('businessSummary') else 'N/A',
            "pe_ratio": info.get('forwardPE', 'N/A'),
            "dividend_yield": info.get('dividendYield', 'N/A'),
            "beta": info.get('beta', 'N/A')
        }
        
        formatted_profile = f"""
Company Profile for {profile['company_name']} ({profile['symbol']}):
- Sector: {profile['sector']}
- Industry: {profile['industry']}
- Market Cap: {profile['market_cap']}
- Revenue: {profile['revenue']}
- Employees: {profile['employees']}
- Headquarters: {profile['headquarters']}
- Website: {profile['website']}
- P/E Ratio: {profile['pe_ratio']}
- Beta: {profile['beta']}
- Dividend Yield: {profile['dividend_yield']}
- Business Summary: {profile['business_summary']}
        """
        
        logger.info(f"Fetched comprehensive company profile for: {company_name}")
        return formatted_profile.strip()
        
    except Exception as e:
        logger.error(f"Error in get_company_profile: {str(e)}")
        return f"Error fetching profile for {company_name}: {str(e)}"

@tool("LatestNewsTool")
def get_latest_news(company_name: str, num_articles: int = 10) -> str:
    """Fetch latest news articles using Serper API with enhanced formatting."""
    if not serper_api_key:
        return "Error: SERPER_API_KEY not found in environment variables."
    
    url = "https://google.serper.dev/news"
    payload = json.dumps({
        "q": f"{company_name} news",
        "num": num_articles,
        "tbs": "qdr:w"  # Last week
    })
    headers = {
        "X-API-KEY": serper_api_key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        response.raise_for_status()
        articles = response.json().get("news", [])
        
        if not articles:
            return f"No recent news found for {company_name}."

        news_summary = f"Latest News for {company_name}:\n\n"
        for i, article in enumerate(articles[:num_articles], 1):
            title = article.get('title', 'No title')
            link = article.get('link', 'No link')
            snippet = article.get('snippet', 'No snippet')
            date = article.get('date', 'No date')
            source = article.get('source', 'Unknown source')
            
            news_summary += f"{i}. {title}\n"
            news_summary += f"   Source: {source} | Date: {date}\n"
            news_summary += f"   Summary: {snippet}\n"
            news_summary += f"   Link: {link}\n\n"

        logger.info(f"Fetched {len(articles)} news articles for: {company_name}")
        
        # Save to log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"news_log_{company_name}_{timestamp}.txt"
        
        with open(log_filename, "w", encoding='utf-8') as log_file:
            log_file.write(news_summary)
        
        return news_summary

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error in get_latest_news: {str(e)}")
        return f"Network error fetching news for {company_name}: {str(e)}"
    except Exception as e:
        logger.error(f"Error in get_latest_news: {str(e)}")
        return f"Error fetching news for {company_name}: {str(e)}"

@tool("DataCollectionTool")
def collect_data_sources(topic: str, data_types: str = "financial,news,social") -> str:
    """Collect structured/unstructured data related to a topic from multiple sources."""
    logger.info(f"Collecting data sources for: {topic}")
    
    data_sources = {
        "financial": [
            "Yahoo Finance",
            "Alpha Vantage",
            "Financial Modeling Prep",
            "IEX Cloud",
            "Quandl"
        ],
        "news": [
            "Google News (via Serper)",
            "NewsAPI",
            "Reuters",
            "Bloomberg Terminal",
            "Financial Times"
        ],
        "social": [
            "Twitter API",
            "Reddit API",
            "StockTwits",
            "Social media sentiment aggregators"
        ],
        "regulatory": [
            "SEC EDGAR",
            "Company annual reports",
            "Regulatory filings",
            "Earnings call transcripts"
        ]
    }
    
    requested_types = [dtype.strip() for dtype in data_types.split(",")]
    
    collection_summary = f"Data Collection Plan for '{topic}':\n\n"
    
    for dtype in requested_types:
        if dtype in data_sources:
            collection_summary += f"{dtype.upper()} DATA SOURCES:\n"
            for source in data_sources[dtype]:
                collection_summary += f"  - {source}\n"
            collection_summary += "\n"
    
    # Add data collection metrics
    collection_summary += "COLLECTION METRICS:\n"
    collection_summary += f"  - Topic: {topic}\n"
    collection_summary += f"  - Data types: {', '.join(requested_types)}\n"
    collection_summary += f"  - Collection date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    collection_summary += f"  - Estimated sources: {sum(len(data_sources[dt]) for dt in requested_types if dt in data_sources)}\n"
    
    return collection_summary

@tool("SentimentAnalysisTool")
def sentiment_analysis(text: str, method: str = "textblob") -> str:
    """Analyze sentiment of the given text using multiple methods."""
    logger.info("Performing sentiment analysis")
    
    if not text or not text.strip():
        return "Error: No text provided for sentiment analysis."
    
    try:
        # Clean the text
        cleaned_text = re.sub(r'[^\w\s]', '', text.lower())
        
        if method == "textblob":
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            if polarity > 0.1:
                sentiment = "Positive"
            elif polarity < -0.1:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"
                
            confidence = abs(polarity)
            
        else:  # Simple keyword-based analysis
            positive_keywords = ['growth', 'profit', 'gain', 'increase', 'rise', 'success', 'strong', 'bullish', 'upgrade']
            negative_keywords = ['loss', 'fall', 'decline', 'decrease', 'drop', 'weak', 'bearish', 'downgrade', 'risk']
            
            positive_count = sum(1 for word in positive_keywords if word in cleaned_text)
            negative_count = sum(1 for word in negative_keywords if word in cleaned_text)
            
            if positive_count > negative_count:
                sentiment = "Positive"
                confidence = positive_count / (positive_count + negative_count + 1)
            elif negative_count > positive_count:
                sentiment = "Negative"
                confidence = negative_count / (positive_count + negative_count + 1)
            else:
                sentiment = "Neutral"
                confidence = 0.5
        
        analysis_result = f"""
Sentiment Analysis Results:
- Overall Sentiment: {sentiment}
- Confidence Score: {confidence:.2f}
- Method Used: {method}
- Text Length: {len(text)} characters
- Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        if method == "textblob":
            analysis_result += f"\n- Polarity: {polarity:.2f} (range: -1 to 1)\n- Subjectivity: {subjectivity:.2f} (range: 0 to 1)"
        
        return analysis_result.strip()
        
    except Exception as e:
        logger.error(f"Error in sentiment_analysis: {str(e)}")
        return f"Error performing sentiment analysis: {str(e)}"

@tool("RiskAssessmentTool")
def assess_risks(company_name: str, risk_categories: str = "market,operational,financial,regulatory") -> str:
    """Provide comprehensive risk assessment of the company."""
    logger.info(f"Assessing risks for: {company_name}")
    
    risk_types = [category.strip() for category in risk_categories.split(",")]
    
    risk_frameworks = {
        "market": [
            "Market volatility and economic downturns",
            "Competitive pressures and market share erosion",
            "Consumer behavior changes",
            "Interest rate fluctuations",
            "Currency exchange rate risks"
        ],
        "operational": [
            "Supply chain disruptions",
            "Cybersecurity threats and data breaches",
            "Key personnel dependency",
            "Technology obsolescence",
            "Quality control issues"
        ],
        "financial": [
            "Liquidity risks and cash flow problems",
            "Credit risk and default probability",
            "Debt burden and leverage ratios",
            "Foreign exchange exposure",
            "Investment and acquisition risks"
        ],
        "regulatory": [
            "Regulatory changes and compliance costs",
            "Environmental regulations",
            "Tax policy changes",
            "Industry-specific regulations",
            "Legal liabilities and litigation"
        ],
        "strategic": [
            "Strategic planning execution risks",
            "Market positioning challenges",
            "Innovation and R&D risks",
            "Merger and acquisition integration",
            "Brand reputation risks"
        ]
    }
    
    assessment = f"Risk Assessment for {company_name}:\n\n"
    
    for risk_type in risk_types:
        if risk_type in risk_frameworks:
            assessment += f"{risk_type.upper()} RISKS:\n"
            for risk in risk_frameworks[risk_type]:
                assessment += f"  • {risk}\n"
            assessment += "\n"
    
    # Add risk scoring framework
    assessment += "RISK SCORING FRAMEWORK:\n"
    assessment += "  • High Risk: Immediate attention required\n"
    assessment += "  • Medium Risk: Monitor closely\n"
    assessment += "  • Low Risk: Routine monitoring\n\n"
    
    assessment += f"Assessment Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    assessment += "Note: This is a general risk framework. Specific company analysis requires detailed financial and operational data."
    
    return assessment

@tool("CompetitorAnalysisTool")
def analyze_competitors(company_name: str, analysis_type: str = "comprehensive") -> str:
    """Benchmark a company with competitors using multiple analysis frameworks."""
    logger.info(f"Analyzing competitors for: {company_name}")
    
    try:
        # Get company info to determine industry
        ticker = yf.Ticker(company_name)
        info = ticker.info
        industry = info.get('industry', 'Technology')
        sector = info.get('sector', 'Technology')
        
        analysis = f"Competitor Analysis for {company_name}:\n\n"
        analysis += f"Industry: {industry}\n"
        analysis += f"Sector: {sector}\n\n"
        
        # Competitive analysis framework
        analysis += "COMPETITIVE ANALYSIS FRAMEWORK:\n\n"
        
        analysis += "1. MARKET POSITION:\n"
        analysis += "   • Market share comparison\n"
        analysis += "   • Brand recognition and reputation\n"
        analysis += "   • Geographic presence\n"
        analysis += "   • Customer base diversity\n\n"
        
        analysis += "2. FINANCIAL PERFORMANCE:\n"
        analysis += "   • Revenue growth rates\n"
        analysis += "   • Profitability margins\n"
        analysis += "   • Return on investment\n"
        analysis += "   • Debt-to-equity ratios\n\n"
        
        analysis += "3. OPERATIONAL EFFICIENCY:\n"
        analysis += "   • Cost structure analysis\n"
        analysis += "   • Supply chain efficiency\n"
        analysis += "   • Technology infrastructure\n"
        analysis += "   • Human resources capabilities\n\n"
        
        analysis += "4. STRATEGIC ADVANTAGES:\n"
        analysis += "   • Pricing strategies\n"
        analysis += "   • Innovation capabilities\n"
        analysis += "   • Distribution channels\n"
        analysis += "   • Strategic partnerships\n\n"
        
        # Industry-specific considerations
        if "technology" in industry.lower():
            analysis += "TECHNOLOGY INDUSTRY SPECIFIC FACTORS:\n"
            analysis += "   • R&D investment levels\n"
            analysis += "   • Patent portfolios\n"
            analysis += "   • Product development cycles\n"
            analysis += "   • Platform ecosystems\n\n"
        
        analysis += f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        analysis += "Note: For detailed competitor analysis, specific financial data and market research are required."
        
        return analysis
        
    except Exception as e:
        logger.error(f"Error in analyze_competitors: {str(e)}")
        return f"Error analyzing competitors for {company_name}: {str(e)}"

@tool("ESGFetcherTool")
def esg_data_fetcher(company_name: str, esg_framework: str = "comprehensive") -> str:
    """Evaluate ESG (Environmental, Social, Governance) performance with detailed metrics."""
    logger.info(f"Fetching ESG data for: {company_name}")
    
    try:
        # Get basic company info
        ticker = yf.Ticker(company_name)
        info = ticker.info
        company_full_name = info.get('longName', company_name)
        industry = info.get('industry', 'N/A')
        
        esg_report = f"ESG Analysis for {company_full_name}:\n\n"
        esg_report += f"Industry: {industry}\n"
        esg_report += f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Environmental Metrics
        esg_report += "ENVIRONMENTAL METRICS:\n"
        esg_report += "  • Carbon Footprint and Emissions\n"
        esg_report += "  • Energy Efficiency and Renewable Energy Usage\n"
        esg_report += "  • Water Usage and Conservation\n"
        esg_report += "  • Waste Management and Recycling\n"
        esg_report += "  • Environmental Compliance Record\n"
        esg_report += "  • Climate Change Risk Assessment\n\n"
        
        # Social Metrics
        esg_report += "SOCIAL METRICS:\n"
        esg_report += "  • Employee Diversity and Inclusion\n"
        esg_report += "  • Workplace Safety and Health\n"
        esg_report += "  • Employee Training and Development\n"
        esg_report += "  • Community Engagement and Philanthropy\n"
        esg_report += "  • Product Safety and Quality\n"
        esg_report += "  • Customer Privacy and Data Protection\n\n"
        
        # Governance Metrics
        esg_report += "GOVERNANCE METRICS:\n"
        esg_report += "  • Board Composition and Independence\n"
        esg_report += "  • Executive Compensation Structure\n"
        esg_report += "  • Audit and Risk Management\n"
        esg_report += "  • Shareholder Rights and Transparency\n"
        esg_report += "  • Business Ethics and Anti-Corruption\n"
        esg_report += "  • Regulatory Compliance\n\n"
        
        # Sample scoring (in real implementation, this would come from ESG data providers)
        esg_report += "SAMPLE ESG SCORING FRAMEWORK:\n"
        esg_report += "  • Environmental Score: 70/100\n"
        esg_report += "  • Social Score: 75/100\n"
        esg_report += "  • Governance Score: 80/100\n"
        esg_report += "  • Overall ESG Score: 75/100\n\n"
        
        esg_report += "ESG DATA SOURCES:\n"
        esg_report += "  • MSCI ESG Research\n"
        esg_report += "  • Sustainalytics\n"
        esg_report += "  • CDP (Carbon Disclosure Project)\n"
        esg_report += "  • Company sustainability reports\n"
        esg_report += "  • Regulatory filings\n\n"
        
        esg_report += "Note: This is a framework for ESG analysis. Actual scores require access to specialized ESG data providers."
        
        return esg_report
        
    except Exception as e:
        logger.error(f"Error in esg_data_fetcher: {str(e)}")
        return f"Error fetching ESG data for {company_name}: {str(e)}"

@tool("MacroeconomicDataTool")
def macroeconomic_data(region: str = "US", indicators: str = "gdp,inflation,unemployment,interest_rates") -> str:
    """Provide comprehensive macroeconomic indicators for a region."""
    logger.info(f"Fetching macroeconomic data for: {region}")
    
    requested_indicators = [indicator.strip() for indicator in indicators.split(",")]
    
    macro_data = f"Macroeconomic Analysis for {region}:\n\n"
    macro_data += f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    indicator_descriptions = {
        "gdp": {
            "name": "Gross Domestic Product (GDP)",
            "sample_value": "2.1% (annualized)",
            "description": "Economic growth rate and total economic output"
        },
        "inflation": {
            "name": "Inflation Rate",
            "sample_value": "3.2% (CPI)",
            "description": "Consumer price index and core inflation measures"
        },
        "unemployment": {
            "name": "Unemployment Rate",
            "sample_value": "3.8%",
            "description": "Labor market conditions and employment levels"
        },
        "interest_rates": {
            "name": "Interest Rates",
            "sample_value": "5.25% (Federal Funds Rate)",
            "description": "Central bank policy rates and bond yields"
        },
        "trade_balance": {
            "name": "Trade Balance",
            "sample_value": "-$68.9B",
            "description": "Import/export balance and trade relationships"
        },
        "currency": {
            "name": "Currency Strength",
            "sample_value": "DXY: 103.45",
            "description": "Exchange rates and currency volatility"
        },
        "manufacturing": {
            "name": "Manufacturing Index",
            "sample_value": "PMI: 48.2",
            "description": "Industrial production and manufacturing activity"
        },
        "consumer_confidence": {
            "name": "Consumer Confidence",
            "sample_value": "105.8",
            "description": "Consumer sentiment and spending patterns"
        }
    }
    
    for indicator in requested_indicators:
        if indicator in indicator_descriptions:
            data = indicator_descriptions[indicator]
            macro_data += f"{data['name'].upper()}:\n"
            macro_data += f"  Current Value: {data['sample_value']}\n"
            macro_data += f"  Description: {data['description']}\n\n"
    
    # Add regional considerations
    regional_factors = {
        "US": ["Federal Reserve policy", "Congressional fiscal policy", "Dollar strength"],
        "EU": ["ECB monetary policy", "Brexit impacts", "Euro stability"],
        "China": ["PBOC policy", "Trade relationships", "Economic reforms"],
        "Global": ["International trade", "Commodity prices", "Geopolitical risks"]
    }
    
    if region in regional_factors:
        macro_data += f"KEY {region} ECONOMIC FACTORS:\n"
        for factor in regional_factors[region]:
            macro_data += f"  • {factor}\n"
        macro_data += "\n"
    
    macro_data += "DATA SOURCES:\n"
    macro_data += "  • Federal Reserve Economic Data (FRED)\n"
    macro_data += "  • Bureau of Economic Analysis (BEA)\n"
    macro_data += "  • International Monetary Fund (IMF)\n"
    macro_data += "  • World Bank\n"
    macro_data += "  • OECD Economic Indicators\n\n"
    
    macro_data += "Note: Sample values shown. Real implementation requires API access to economic data providers."
    
    return macro_data

# Additional utility functions for enhanced functionality
def format_currency(value: float) -> str:
    """Format currency values with appropriate suffixes."""
    if value >= 1e12:
        return f"${value/1e12:.1f}T"
    elif value >= 1e9:
        return f"${value/1e9:.1f}B"
    elif value >= 1e6:
        return f"${value/1e6:.1f}M"
    elif value >= 1e3:
        return f"${value/1e3:.1f}K"
    else:
        return f"${value:.2f}"

def calculate_volatility(prices: List[float]) -> float:
    """Calculate price volatility from historical prices."""
    if len(prices) < 2:
        return 0.0
    
    returns = [(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, len(prices))]
    avg_return = sum(returns) / len(returns)
    variance = sum((r - avg_return) ** 2 for r in returns) / len(returns)
    return variance ** 0.5

# Export all tools for easy importing
__all__ = [
    'get_company_profile',
    'get_latest_news',
    'collect_data_sources',
    'sentiment_analysis',
    'assess_risks',
    'analyze_competitors',
    'esg_data_fetcher',
    'macroeconomic_data'
]