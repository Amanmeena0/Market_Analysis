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
import logging
from typing import List, Dict, Any

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Handle asyncio event loop
try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# Initialize LLM with enhanced configuration
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.environ.get("GOOGLE_API_KEY"),
    temperature=0.3,  # Lower temperature for more consistent analysis
    verbose=True,
    max_tokens=4000,  # Increased token limit for comprehensive analysis
    top_p=0.9,
    top_k=40
)

# Utility functions
def format_datasets(datasets: List[Dict[str, Any]]) -> str:
    """Format datasets for better readability and structure."""
    if not datasets:
        return "No datasets available.\n"
    
    formatted_output = "=" * 80 + "\n"
    formatted_output += "DATASET COLLECTION SUMMARY\n"
    formatted_output += "=" * 80 + "\n\n"
    
    for i, dataset in enumerate(datasets, 1):
        title = dataset.get("title", "Unknown Title")
        description = dataset.get("description", "No description available.")
        links = dataset.get("links", [])
        source = dataset.get("source", "Unknown Source")
        date = dataset.get("date", "Unknown Date")
        
        formatted_output += f"{i}. {title}\n"
        formatted_output += f"   Source: {source}\n"
        formatted_output += f"   Date: {date}\n"
        formatted_output += f"   Description: {description}\n"
        
        if links:
            formatted_output += "   Links:\n"
            for link in links[:3]:  # Limit to top 3 links
                formatted_output += f"     • {link}\n"
        
        formatted_output += "\n" + "-" * 60 + "\n\n"
    
    return formatted_output

def create_agent_with_fallback(role: str, goal: str, backstory: str, tools: List, **kwargs) -> Agent:
    """Create an agent with error handling and fallback configuration."""
    try:
        return Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=tools,
            verbose=True,
            memory=True,
            llm=llm,
            max_iter=3,  # Limit iterations to prevent infinite loops
            max_execution_time=300,  # 5 minutes timeout
            **kwargs
        )
    except Exception as e:
        logger.error(f"Error creating agent {role}: {str(e)}")
        raise

# =============================================================================
# CORE ANALYSIS AGENTS
# =============================================================================

research_agent = create_agent_with_fallback(
    role="Senior Market Research Analyst",
    goal="Conduct comprehensive financial and market research for target companies, "
         "gathering all relevant data points for informed investment decisions",
    backstory="You are a seasoned market research analyst with 15+ years of experience "
              "in financial markets. You specialize in gathering comprehensive company "
              "profiles, analyzing market positioning, and identifying key financial metrics. "
              "Your expertise includes fundamental analysis, market trends, and competitive "
              "landscape assessment.",
    tools=[get_company_profile, get_latest_news, collect_data_sources],
    allow_delegation=True
)

modeling_agent = create_agent_with_fallback(
    role="Quantitative Financial Modeler",
    goal="Build sophisticated financial models, perform valuation analysis, and "
         "generate actionable investment recommendations based on comprehensive data",
    backstory="You are a quantitative analyst with expertise in financial modeling, "
              "DCF analysis, and statistical forecasting. You have a strong background "
              "in mathematics, statistics, and financial theory. Your models are known "
              "for their accuracy and have been used by major investment firms for "
              "portfolio optimization and risk management.",
    tools=[get_latest_news, collect_data_sources, macroeconomic_data],
    allow_delegation=True
)

report_agent = create_agent_with_fallback(
    role="Executive Financial Report Writer",
    goal="Transform complex financial analysis into clear, executive-level reports "
         "that drive strategic decision-making",
    backstory="You are an experienced financial writer who has worked with top-tier "
              "investment banks and consulting firms. You excel at distilling complex "
              "financial analysis into compelling narratives that C-suite executives "
              "can quickly understand and act upon. Your reports are known for their "
              "clarity, insight, and actionable recommendations.",
    tools=[get_latest_news, sentiment_analysis],
    allow_delegation=True
)

# =============================================================================
# SPECIALIZED ANALYSIS AGENTS
# =============================================================================

data_collection_agent = create_agent_with_fallback(
    role="Data Intelligence Specialist",
    goal="Systematically collect, validate, and structure data from multiple sources "
         "to create a comprehensive information foundation for analysis",
    backstory="You are a data specialist with expertise in financial data aggregation, "
              "API integration, and data quality assurance. You have experience working "
              "with Bloomberg terminals, Reuters, and various financial databases. "
              "Your strength lies in identifying the most relevant and reliable data "
              "sources for any given analysis requirement.",
    tools=[collect_data_sources, get_company_profile],
    allow_delegation=False
)

sentiment_analysis_agent = create_agent_with_fallback(
    role="Market Sentiment Analyst",
    goal="Analyze market sentiment, news sentiment, and social media trends to "
         "gauge investor confidence and market psychology",
    backstory="You are a data scientist specializing in natural language processing "
              "and sentiment analysis. You have developed proprietary models for "
              "analyzing financial news, social media, and market communications. "
              "Your insights help predict market movements and investor behavior "
              "patterns that traditional analysis might miss.",
    tools=[sentiment_analysis, get_latest_news],
    allow_delegation=False
)

risk_assessment_agent = create_agent_with_fallback(
    role="Chief Risk Assessment Officer",
    goal="Identify, quantify, and prioritize all potential risks that could impact "
         "investment performance and recommend mitigation strategies",
    backstory="You are a risk management expert with experience at major investment "
              "banks and hedge funds. You specialize in market risk, credit risk, "
              "operational risk, and regulatory risk assessment. Your risk models "
              "have helped institutions avoid major losses during market downturns "
              "and identify emerging threats before they materialize.",
    tools=[assess_risks, get_latest_news, macroeconomic_data],
    allow_delegation=False
)

competitor_analysis_agent = create_agent_with_fallback(
    role="Competitive Intelligence Analyst",
    goal="Conduct thorough competitive analysis to benchmark performance and "
         "identify strategic advantages and threats in the market",
    backstory="You are a competitive intelligence expert with deep knowledge of "
              "industry dynamics across multiple sectors. You have access to "
              "comprehensive competitive databases and have developed frameworks "
              "for analyzing competitive positioning, market share dynamics, and "
              "strategic differentiation. Your analysis helps identify investment "
              "opportunities and competitive moats.",
    tools=[analyze_competitors, get_company_profile, get_latest_news],
    allow_delegation=False
)

esg_analyst_agent = create_agent_with_fallback(
    role="ESG Research Specialist",
    goal="Evaluate environmental, social, and governance factors to assess "
         "long-term sustainability and ESG investment attractiveness",
    backstory="You are an ESG specialist with expertise in sustainability reporting, "
              "ESG scoring methodologies, and regulatory compliance. You have worked "
              "with institutional investors to integrate ESG factors into investment "
              "decisions. Your analysis helps identify companies with strong ESG "
              "practices that may outperform in the long term and avoid ESG-related "
              "risks that could impact valuations.",
    tools=[esg_data_fetcher, get_latest_news, assess_risks],
    allow_delegation=False
)

macroeconomic_analyst_agent = create_agent_with_fallback(
    role="Senior Macroeconomic Strategist",
    goal="Analyze macroeconomic trends and their impact on investment opportunities, "
         "providing context for market conditions and economic cycles",
    backstory="You are a macroeconomic analyst with experience at central banks and "
              "major investment firms. You specialize in analyzing monetary policy, "
              "fiscal policy, and global economic trends. Your insights help predict "
              "market cycles, interest rate movements, and currency fluctuations that "
              "impact investment performance across different asset classes and regions.",
    tools=[macroeconomic_data, get_latest_news, assess_risks],
    allow_delegation=False
)

# =============================================================================
# AGENT ORCHESTRATION AND MANAGEMENT
# =============================================================================

class AgentManager:
    """Manages agent interactions and coordinates analysis workflows."""
    
    def __init__(self):
        self.core_agents = {
            'research': research_agent,
            'modeling': modeling_agent,
            'report': report_agent
        }
        
        self.specialized_agents = {
            'data_collection': data_collection_agent,
            'sentiment': sentiment_analysis_agent,
            'risk': risk_assessment_agent,
            'competitor': competitor_analysis_agent,
            'esg': esg_analyst_agent,
            'macro': macroeconomic_analyst_agent
        }
        
        self.all_agents = {**self.core_agents, **self.specialized_agents}
    
    def get_agent(self, agent_name: str) -> Agent:
        """Retrieve a specific agent by name."""
        return self.all_agents.get(agent_name)
    
    def get_core_agents(self) -> Dict[str, Agent]:
        """Get all core analysis agents."""
        return self.core_agents
    
    def get_specialized_agents(self) -> Dict[str, Agent]:
        """Get all specialized analysis agents."""
        return self.specialized_agents
    
    def get_analysis_chain(self, analysis_type: str = "comprehensive") -> List[Agent]:
        """Get recommended agent chain for different analysis types."""
        chains = {
            "comprehensive": [
                data_collection_agent,
                research_agent,
                sentiment_analysis_agent,
                risk_assessment_agent,
                competitor_analysis_agent,
                esg_analyst_agent,
                macroeconomic_analyst_agent,
                modeling_agent,
                report_agent
            ],
            "quick": [
                research_agent,
                modeling_agent,
                report_agent
            ],
            "risk_focused": [
                data_collection_agent,
                research_agent,
                risk_assessment_agent,
                macroeconomic_analyst_agent,
                modeling_agent,
                report_agent
            ],
            "esg_focused": [
                research_agent,
                esg_analyst_agent,
                sentiment_analysis_agent,
                risk_assessment_agent,
                report_agent
            ]
        }
        
        return chains.get(analysis_type, chains["comprehensive"])

# =============================================================================
# AGENT CONFIGURATION TEMPLATES
# =============================================================================

AGENT_CONFIGURATIONS = {
    "conservative": {
        "temperature": 0.1,
        "max_iter": 2,
        "focus": "risk_mitigation"
    },
    "aggressive": {
        "temperature": 0.5,
        "max_iter": 5,
        "focus": "opportunity_identification"
    },
    "balanced": {
        "temperature": 0.3,
        "max_iter": 3,
        "focus": "comprehensive_analysis"
    }
}

# Initialize agent manager
agent_manager = AgentManager()

# Export key components
__all__ = [
    'research_agent',
    'modeling_agent', 
    'report_agent',
    'data_collection_agent',
    'sentiment_analysis_agent',
    'risk_assessment_agent',
    'competitor_analysis_agent',
    'esg_analyst_agent',
    'macroeconomic_analyst_agent',
    'agent_manager',
    'format_datasets',
    'AGENT_CONFIGURATIONS'
]

# Logging initialization complete
logger.info("All agents initialized successfully")
logger.info(f"Core agents: {list(agent_manager.core_agents.keys())}")
logger.info(f"Specialized agents: {list(agent_manager.specialized_agents.keys())}")