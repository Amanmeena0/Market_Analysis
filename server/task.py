from crewai import Task
from agents import (
    research_agent, modeling_agent, report_agent,
    data_collection_agent, sentiment_analysis_agent,
    risk_assessment_agent, competitor_analysis_agent,
    esg_analyst_agent, macroeconomic_analyst_agent
)
from tools import (
    get_latest_news, get_company_profile,
    collect_data_sources, sentiment_analysis,
    assess_risks, analyze_competitors,
    esg_data_fetcher, macroeconomic_data
)
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskManager:
    """Manages task creation, dependencies, and execution workflows."""
    
    def __init__(self):
        self.task_registry = {}
        self.execution_metrics = {}
    
    def register_task(self, task_id: str, task: Task) -> None:
        """Register a task in the task registry."""
        self.task_registry[task_id] = task
        logger.info(f"Registered task: {task_id}")
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by ID."""
        return self.task_registry.get(task_id)
    
    def get_execution_metrics(self) -> Dict[str, Any]:
        """Get execution metrics for all tasks."""
        return self.execution_metrics

def create_output_template(task_type: str, company: str) -> str:
    """Create standardized output templates for different task types."""
    templates = {
        "data_collection": f"""
## Data Collection Report for {company}
### Executive Summary
- Total sources identified: [NUMBER]
- Data quality assessment: [HIGH/MEDIUM/LOW]
- Key data gaps identified: [LIST]

### Data Sources Inventory
1. **Financial Data Sources**
   - [Source 1]: [Description and accessibility]
   - [Source 2]: [Description and accessibility]

2. **Market Data Sources**
   - [Source 1]: [Description and accessibility]
   - [Source 2]: [Description and accessibility]

3. **News and Media Sources**
   - [Source 1]: [Description and accessibility]
   - [Source 2]: [Description and accessibility]

### Data Quality Assessment
- Completeness: [SCORE/10]
- Accuracy: [SCORE/10]
- Timeliness: [SCORE/10]
- Relevance: [SCORE/10]

### Recommendations
- [Recommendation 1]
- [Recommendation 2]
        """,
        
        "research": f"""
## Market Research Analysis for {company}
### Company Overview
- Full Name: [COMPANY NAME]
- Ticker: [SYMBOL]
- Market Cap: [VALUE]
- Sector: [SECTOR]
- Industry: [INDUSTRY]

### Key Financial Metrics
- Revenue (TTM): [VALUE]
- Net Income: [VALUE]
- P/E Ratio: [VALUE]
- Debt-to-Equity: [VALUE]
- ROE: [VALUE]

### Market Position
- Market Share: [PERCENTAGE]
- Competitive Ranking: [POSITION]
- Geographic Presence: [REGIONS]

### Recent Developments
- [Development 1 with date]
- [Development 2 with date]
- [Development 3 with date]

### Investment Thesis
- Bull Case: [POINTS]
- Bear Case: [POINTS]
        """,
        
        "sentiment": f"""
## Sentiment Analysis Report for {company}
### Overall Sentiment Score: [SCORE] ([POSITIVE/NEGATIVE/NEUTRAL])

### Sentiment Breakdown
- **News Media**: [SCORE] ([POSITIVE/NEGATIVE/NEUTRAL])
- **Social Media**: [SCORE] ([POSITIVE/NEGATIVE/NEUTRAL])
- **Analyst Reports**: [SCORE] ([POSITIVE/NEGATIVE/NEUTRAL])
- **Investor Communications**: [SCORE] ([POSITIVE/NEGATIVE/NEUTRAL])

### Key Sentiment Drivers
**Positive Drivers:**
- [Driver 1]
- [Driver 2]

**Negative Drivers:**
- [Driver 1]
- [Driver 2]

### Sentiment Trends
- 30-day trend: [IMPROVING/DETERIORATING/STABLE]
- 90-day trend: [IMPROVING/DETERIORATING/STABLE]

### Market Impact Assessment
- Potential impact on stock price: [HIGH/MEDIUM/LOW]
- Recommendation: [BUY/HOLD/SELL consideration based on sentiment]
        """,
        
        "risk": f"""
## Risk Assessment Report for {company}
### Risk Summary
- Overall Risk Level: [HIGH/MEDIUM/LOW]
- Risk Score: [SCORE/100]

### Top 5 Identified Risks
1. **[Risk Category]**: [Risk Name]
   - Impact: [HIGH/MEDIUM/LOW]
   - Probability: [HIGH/MEDIUM/LOW]
   - Mitigation: [Strategy]

2. **[Risk Category]**: [Risk Name]
   - Impact: [HIGH/MEDIUM/LOW]
   - Probability: [HIGH/MEDIUM/LOW]
   - Mitigation: [Strategy]

[Continue for risks 3-5]

### Risk Categories Analysis
- **Market Risk**: [SCORE/10]
- **Operational Risk**: [SCORE/10]
- **Financial Risk**: [SCORE/10]
- **Regulatory Risk**: [SCORE/10]
- **Strategic Risk**: [SCORE/10]

### Risk Monitoring Recommendations
- [Recommendation 1]
- [Recommendation 2]
        """,
        
        "competitor": f"""
## Competitive Analysis Report for {company}
### Competitive Landscape Overview
- Industry: [INDUSTRY]
- Market Size: [VALUE]
- Growth Rate: [PERCENTAGE]
- Key Success Factors: [LIST]

### Competitive Positioning
**{company} vs. Key Competitors:**

| Metric | {company} | Competitor 1 | Competitor 2 | Competitor 3 |
|--------|-----------|--------------|--------------|--------------|
| Revenue | [VALUE] | [VALUE] | [VALUE] | [VALUE] |
| Market Share | [%] | [%] | [%] | [%] |
| Profit Margin | [%] | [%] | [%] | [%] |
| ROE | [%] | [%] | [%] | [%] |

### Competitive Advantages
**{company}'s Strengths:**
- [Strength 1]
- [Strength 2]

**{company}'s Weaknesses:**
- [Weakness 1]
- [Weakness 2]

### Strategic Recommendations
- [Recommendation 1]
- [Recommendation 2]
        """,
        
        "esg": f"""
## ESG Analysis Report for {company}
### ESG Overall Score: [SCORE/100]

### Component Scores
- **Environmental**: [SCORE/100]
- **Social**: [SCORE/100]
- **Governance**: [SCORE/100]

### Environmental Performance
- Carbon Footprint: [ASSESSMENT]
- Renewable Energy Usage: [PERCENTAGE]
- Waste Management: [ASSESSMENT]
- Water Usage: [ASSESSMENT]

### Social Performance
- Employee Diversity: [METRICS]
- Workplace Safety: [METRICS]
- Community Engagement: [ASSESSMENT]
- Product Safety: [ASSESSMENT]

### Governance Performance
- Board Independence: [PERCENTAGE]
- Executive Compensation: [ASSESSMENT]
- Audit Quality: [ASSESSMENT]
- Shareholder Rights: [ASSESSMENT]

### ESG Investment Implications
- ESG Risk Level: [HIGH/MEDIUM/LOW]
- Regulatory Compliance: [STRONG/ADEQUATE/WEAK]
- Sustainability Trends: [IMPROVING/STABLE/DETERIORATING]
        """,
        
        "macro": f"""
## Macroeconomic Analysis Report
### Economic Environment Assessment
- Overall Economic Health: [STRONG/MODERATE/WEAK]
- Economic Cycle Stage: [EXPANSION/PEAK/CONTRACTION/TROUGH]

### Key Economic Indicators
- GDP Growth Rate: [PERCENTAGE]
- Inflation Rate: [PERCENTAGE]
- Unemployment Rate: [PERCENTAGE]
- Interest Rates: [PERCENTAGE]
- Currency Strength: [STRONG/MODERATE/WEAK]

### Industry Impact Analysis
**Impact on {company}'s Industry:**
- Demand Sensitivity: [HIGH/MEDIUM/LOW]
- Cost Structure Impact: [HIGH/MEDIUM/LOW]
- Competitive Dynamics: [FAVORABLE/NEUTRAL/UNFAVORABLE]

### Economic Forecasts
- 12-month outlook: [POSITIVE/NEUTRAL/NEGATIVE]
- Key risks: [LIST]
- Key opportunities: [LIST]

### Investment Implications
- Sector allocation recommendation: [OVERWEIGHT/NEUTRAL/UNDERWEIGHT]
- Timing considerations: [IMMEDIATE/WAIT/GRADUAL]
        """,
        
        "modeling": f"""
## Financial Modeling and Valuation Report for {company}
### Valuation Summary
- Current Price: $[PRICE]
- Target Price: $[PRICE]
- Recommendation: [BUY/HOLD/SELL]
- Upside/Downside: [PERCENTAGE]

### DCF Analysis
- Terminal Value: $[VALUE]
- Present Value of FCF: $[VALUE]
- Enterprise Value: $[VALUE]
- Equity Value: $[VALUE]
- Price per Share: $[PRICE]

### Valuation Multiples
- P/E Ratio: [VALUE] vs Industry [VALUE]
- P/B Ratio: [VALUE] vs Industry [VALUE]
- EV/EBITDA: [VALUE] vs Industry [VALUE]
- PEG Ratio: [VALUE]

### Financial Forecasts (3-Year)
| Metric | Year 1 | Year 2 | Year 3 |
|--------|--------|--------|--------|
| Revenue | $[VALUE] | $[VALUE] | $[VALUE] |
| EBITDA | $[VALUE] | $[VALUE] | $[VALUE] |
| Net Income | $[VALUE] | $[VALUE] | $[VALUE] |
| EPS | $[VALUE] | $[VALUE] | $[VALUE] |

### Key Assumptions
- Revenue Growth: [PERCENTAGE]
- Margin Assumptions: [DETAILS]
- WACC: [PERCENTAGE]
- Terminal Growth: [PERCENTAGE]

### Sensitivity Analysis
- Base Case: $[PRICE]
- Bull Case: $[PRICE]
- Bear Case: $[PRICE]
        """,
        
        "report": f"""
# Executive Investment Report: {company}
## Investment Recommendation: [BUY/HOLD/SELL]

### Executive Summary
[2-3 paragraph summary of key findings and recommendation]

### Key Investment Highlights
- **Valuation**: [Price target and current assessment]
- **Business Quality**: [Assessment of competitive position]
- **Growth Prospects**: [Revenue and earnings growth outlook]
- **Risk Profile**: [Key risks and mitigation factors]
- **ESG Considerations**: [Sustainability and governance factors]

### Financial Performance
[Summary of key financial metrics and trends]

### Market Position and Competition
[Assessment of competitive landscape and market position]

### Risk Assessment
[Top 3-5 key risks with impact assessment]

### Macroeconomic Considerations
[How economic factors affect the investment thesis]

### ESG Profile
[Environmental, social, and governance assessment]

### Valuation Analysis
[DCF results, multiples analysis, and price target]

### Investment Recommendation
**Recommendation**: [BUY/HOLD/SELL]
**Price Target**: $[PRICE]
**Time Horizon**: [PERIOD]
**Risk Level**: [HIGH/MEDIUM/LOW]

### Action Items
1. [Specific action item 1]
2. [Specific action item 2]
3. [Specific action item 3]
        """
    }
    
    return templates.get(task_type, f"Analysis report for {company}")

def define_tasks(company: str, analysis_type: str = "comprehensive", custom_config: Dict[str, Any] = None) -> List[Task]:
    """
    Define tasks for financial analysis with enhanced configurations.
    
    Args:
        company: Company name or ticker symbol
        analysis_type: Type of analysis (comprehensive, quick, risk_focused, esg_focused)
        custom_config: Custom configuration parameters
    
    Returns:
        List of Task objects configured for the analysis
    """
    
    if custom_config is None:
        custom_config = {}
    
    # Initialize task manager
    task_manager = TaskManager()
    
    # Default configuration
    default_config = {
        "output_format": "structured",
        "detail_level": "high",
        "include_charts": True,
        "include_recommendations": True
    }
    
    # Merge configurations
    config = {**default_config, **custom_config}
    
    tasks = []
    
    # Task 1: Data Collection Task
    data_collection_task = Task(
        description=f"""
        Conduct comprehensive data collection for {company} analysis.
        
        **Objectives:**
        1. Identify and catalog all relevant data sources
        2. Assess data quality and completeness
        3. Prioritize data sources based on reliability and relevance
        4. Document any data gaps or limitations
        
        **Data Categories to Collect:**
        - Financial statements and SEC filings
        - Market data and trading information
        - News articles and media coverage
        - Analyst reports and research
        - Industry reports and benchmarks
        - ESG and sustainability data
        - Macroeconomic indicators
        
        **Quality Standards:**
        - Ensure data freshness (prefer recent data)
        - Verify source credibility
        - Document data collection methodology
        - Identify potential biases or limitations
        """,
        expected_output=create_output_template("data_collection", company),
        tools=[collect_data_sources, get_company_profile],
        agent=data_collection_agent,
        output_file=f"data_collection_{company}_{datetime.now().strftime('%Y%m%d')}.md"
    )
    tasks.append(data_collection_task)
    task_manager.register_task("data_collection", data_collection_task)

    # Task 2: Market Research Task
    market_research_task = Task(
        description=f"""
        Conduct comprehensive market research and fundamental analysis for {company}.
        
        **Research Scope:**
        1. Company profile and business model analysis
        2. Financial performance and key metrics
        3. Market position and competitive landscape
        4. Recent developments and news analysis
        5. Management team and corporate governance
        
        **Key Focus Areas:**
        - Revenue streams and business segments
        - Profitability and margin analysis
        - Balance sheet strength and capital structure
        - Cash flow generation and capital allocation
        - Growth drivers and strategic initiatives
        
        **Analysis Requirements:**
        - Compare metrics to industry benchmarks
        - Identify trends and patterns in financial data
        - Assess business model sustainability
        - Evaluate management effectiveness
        """,
        expected_output=create_output_template("research", company),
        tools=[get_company_profile, get_latest_news, collect_data_sources],
        agent=research_agent,
        context=[data_collection_task],
        output_file=f"market_research_{company}_{datetime.now().strftime('%Y%m%d')}.md"
    )
    tasks.append(market_research_task)
    task_manager.register_task("market_research", market_research_task)

    # Task 3: Sentiment Analysis Task
    sentiment_analysis_task = Task(
        description=f"""
        Perform comprehensive sentiment analysis for {company} across multiple channels.
        
        **Analysis Scope:**
        1. News media sentiment analysis
        2. Social media sentiment tracking
        3. Analyst report sentiment assessment
        4. Investor communication sentiment
        5. Earnings call sentiment analysis
        
        **Methodology:**
        - Use multiple sentiment analysis techniques
        - Analyze sentiment trends over time
        - Identify key sentiment drivers
        - Assess sentiment reliability and confidence
        - Compare sentiment to stock price movements
        
        **Deliverables:**
        - Overall sentiment score and classification
        - Sentiment breakdown by source type
        - Key positive and negative sentiment drivers
        - Sentiment trend analysis
        - Market impact assessment
        """,
        expected_output=create_output_template("sentiment", company),
        tools=[sentiment_analysis, get_latest_news],
        agent=sentiment_analysis_agent,
        context=[market_research_task],
        output_file=f"sentiment_analysis_{company}_{datetime.now().strftime('%Y%m%d')}.md"
    )
    tasks.append(sentiment_analysis_task)
    task_manager.register_task("sentiment_analysis", sentiment_analysis_task)

    # Task 4: Risk Assessment Task
    risk_assessment_task = Task(
        description=f"""
        Conduct comprehensive risk assessment for {company} investment.
        
        **Risk Categories to Analyze:**
        1. Market Risk (systematic and unsystematic)
        2. Operational Risk (business operations)
        3. Financial Risk (leverage, liquidity, credit)
        4. Regulatory Risk (compliance, policy changes)
        5. Strategic Risk (competitive, execution)
        6. ESG Risk (environmental, social, governance)
        7. Geopolitical Risk (regional, trade, currency)
        
        **Risk Assessment Framework:**
        - Identify and categorize all material risks
        - Assess probability and potential impact
        - Evaluate current risk mitigation measures
        - Recommend additional risk management strategies
        - Provide risk scoring and ranking
        
        **Analysis Requirements:**
        - Quantify risks where possible
        - Consider risk interdependencies
        - Assess risk timeline and urgency
        - Benchmark against industry peers
        """,
        expected_output=create_output_template("risk", company),
        tools=[assess_risks, get_latest_news, macroeconomic_data],
        agent=risk_assessment_agent,
        context=[market_research_task, sentiment_analysis_task],
        output_file=f"risk_assessment_{company}_{datetime.now().strftime('%Y%m%d')}.md"
    )
    tasks.append(risk_assessment_task)
    task_manager.register_task("risk_assessment", risk_assessment_task)

    # Task 5: Competitor Analysis Task
    competitor_analysis_task = Task(
        description=f"""
        Conduct detailed competitive analysis for {company}.
        
        **Competitive Analysis Framework:**
        1. Industry landscape and market structure
        2. Key competitor identification and profiling
        3. Competitive positioning analysis
        4. Financial performance comparison
        5. Strategic initiative comparison
        6. Market share and growth analysis
        7. Competitive advantages and moats
        
        **Comparison Metrics:**
        - Financial performance (revenue, margins, ROE)
        - Operational efficiency (asset utilization, productivity)
        - Market position (share, growth, customer base)
        - Strategic positioning (differentiation, innovation)
        - Management effectiveness (execution, capital allocation)
        
        **Deliverables:**
        - Competitive landscape overview
        - Detailed competitor comparison matrix
        - {company}'s competitive advantages and disadvantages
        - Strategic recommendations for competitive positioning
        """,
        expected_output=create_output_template("competitor", company),
        tools=[analyze_competitors, get_company_profile, get_latest_news],
        agent=competitor_analysis_agent,
        context=[market_research_task],
        output_file=f"competitor_analysis_{company}_{datetime.now().strftime('%Y%m%d')}.md"
    )
    tasks.append(competitor_analysis_task)
    task_manager.register_task("competitor_analysis", competitor_analysis_task)

    # Task 6: ESG Analysis Task
    esg_analysis_task = Task(
        description=f"""
        Evaluate {company}'s ESG (Environmental, Social, Governance) performance.
        
        **ESG Assessment Framework:**
        
        **Environmental Analysis:**
        - Carbon footprint and emissions
        - Energy efficiency and renewable energy
        - Water usage and conservation
        - Waste management and circular economy
        - Environmental compliance and risks
        
        **Social Analysis:**
        - Employee diversity and inclusion
        - Workplace safety and health
        - Human rights and labor practices
        - Community engagement and impact
        - Product safety and customer welfare
        
        **Governance Analysis:**
        - Board composition and independence
        - Executive compensation structure
        - Audit quality and financial transparency
        - Shareholder rights and engagement
        - Business ethics and compliance
        
        **ESG Integration:**
        - ESG risk assessment for investment
        - Regulatory compliance evaluation
        - Sustainability trend analysis
        - ESG score calculation and benchmarking
        """,
        expected_output=create_output_template("esg", company),
        tools=[esg_data_fetcher, get_latest_news, assess_risks],
        agent=esg_analyst_agent,
        context=[market_research_task, risk_assessment_task],
        output_file=f"esg_analysis_{company}_{datetime.now().strftime('%Y%m%d')}.md"
    )
    tasks.append(esg_analysis_task)
    task_manager.register_task("esg_analysis", esg_analysis_task)

    # Task 7: Macroeconomic Analysis Task
    macro_analysis_task = Task(
        description=f"""
        Analyze macroeconomic factors affecting {company} and its industry.
        
        **Macroeconomic Analysis Scope:**
        1. Current economic environment assessment
        2. Key economic indicators analysis
        3. Economic cycle and timing considerations
        4. Industry-specific economic impacts
        5. Regional and global economic factors
        6. Economic forecasts and scenarios
        
        **Key Economic Indicators:**
        - GDP growth and economic output
        - Inflation rates and price levels
        - Interest rates and monetary policy
        - Employment and labor market conditions
        - Currency exchange rates
        - Commodity prices and supply chains
        
        **Industry Impact Analysis:**
        - Economic sensitivity assessment
        - Demand elasticity and cyclicality
        - Cost structure impacts
        - Competitive dynamics changes
        - Regional exposure analysis
        
        **Investment Implications:**
        - Economic scenario planning
        - Sector rotation considerations
        - Timing and positioning recommendations
        """,
        expected_output=create_output_template("macro", company),
        tools=[macroeconomic_data, get_latest_news, assess_risks],
        agent=macroeconomic_analyst_agent,
        context=[market_research_task, risk_assessment_task],
        output_file=f"macro_analysis_{company}_{datetime.now().strftime('%Y%m%d')}.md"
    )
    tasks.append(macro_analysis_task)
    task_manager.register_task("macro_analysis", macro_analysis_task)

    # Task 8: Financial Modeling Task
    financial_modeling_task = Task(
        description=f"""
        Build comprehensive financial models and valuation analysis for {company}.
        
        **Financial Modeling Scope:**
        1. Historical financial analysis and trends
        2. Three-statement financial model construction
        3. DCF (Discounted Cash Flow) valuation model
        4. Comparable company analysis
        5. Sensitivity and scenario analysis
        6. Valuation reconciliation and price target
        
        **Model Components:**
        - Income statement projections (3-5 years)
        - Balance sheet projections
        - Cash flow statement projections
        - Key ratio analysis and trends
        - Working capital requirements
        - Capital expenditure planning
        
        **Valuation Methodology:**
        - DCF analysis with terminal value
        - Multiple valuation approaches (P/E, EV/EBITDA, P/B)
        - Sum-of-the-parts analysis (if applicable)
        - Asset-based valuation (if relevant)
        - Scenario analysis (bull, base, bear cases)
        
        **Key Assumptions:**
        - Revenue growth rates and drivers
        - Margin assumptions and cost structure
        - Working capital efficiency
        - Capital allocation strategy
        - Discount rate (WACC) calculation
        - Terminal growth rate assumptions
        """,
        expected_output=create_output_template("modeling", company),
        tools=[get_latest_news, collect_data_sources, macroeconomic_data],
        agent=modeling_agent,
        context=[market_research_task, risk_assessment_task, competitor_analysis_task, macro_analysis_task],
        output_file=f"financial_model_{company}_{datetime.now().strftime('%Y%m%d')}.md"
    )
    tasks.append(financial_modeling_task)
    task_manager.register_task("financial_modeling", financial_modeling_task)

    # Task 9: Report Generation Task
    report_generation_task = Task(
        description=f"""
        Compile comprehensive executive investment report for {company}.
        
        **Report Structure:**
        1. Executive Summary and Investment Recommendation
        2. Company Overview and Business Analysis
        3. Financial Performance and Valuation
        4. Market Position and Competitive Analysis
        5. Risk Assessment and Mitigation
        6. ESG Considerations and Sustainability
        7. Macroeconomic Context and Industry Outlook
        8. Investment Thesis and Recommendation
        9. Action Items and Monitoring Plan
        
        **Report Requirements:**
        - Executive-level clarity and conciseness
        - Data-driven insights and analysis
        - Clear investment recommendation with rationale
        - Risk-adjusted return expectations
        - Specific action items and timelines
        - Professional formatting and visualization
        
        **Key Deliverables:**
        - Clear BUY/HOLD/SELL recommendation
        - Price target with confidence intervals
        - Risk assessment and mitigation strategies
        - Portfolio allocation recommendations
        - Monitoring and review schedule
        
        **Quality Standards:**
        - Logical flow and coherent narrative
        - Balanced presentation of opportunities and risks
        - Actionable insights and recommendations
        - Professional presentation suitable for stakeholders
        """,
        expected_output=create_output_template("report", company),
        tools=[get_latest_news, sentiment_analysis],
        agent=report_agent,
        context=[
            market_research_task,
            sentiment_analysis_task,
            risk_assessment_task,
            competitor_analysis_task,
            esg_analysis_task,
            macro_analysis_task,
            financial_modeling_task
        ],
        output_file=f"executive_report_{company}_{datetime.now().strftime('%Y%m%d')}.md"
    )
    tasks.append(report_generation_task)
    task_manager.register_task("report_generation", report_generation_task)

    # Filter tasks based on analysis type
    if analysis_type == "quick":
        tasks = [market_research_task, financial_modeling_task, report_generation_task]
    elif analysis_type == "risk_focused":
        tasks = [
            data_collection_task,
            market_research_task,
            risk_assessment_task,
            macro_analysis_task,
            financial_modeling_task,
            report_generation_task
        ]
    elif analysis_type == "esg_focused":
        tasks = [
            market_research_task,
            esg_analysis_task,
            sentiment_analysis_task,
            risk_assessment_task,
            report_generation_task
        ]
    # comprehensive analysis includes all tasks (default)
    
    logger.info(f"Created {len(tasks)} tasks for {analysis_type} analysis of {company}")
    return tasks

def create_custom_task(
    task_id: str,
    description: str,
    expected_output: str,
    agent,
    tools: List = None,
    context: List[Task] = None,
    **kwargs
) -> Task:
    """Create a custom task with standardized configuration."""
    
    if tools is None:
        tools = []
    
    if context is None:
        context = []
    
    custom_task = Task(
        description=description,
        expected_output=expected_output,
        tools=tools,
        agent=agent,
        context=context,
        **kwargs
    )
    
    logger.info(f"Created custom task: {task_id}")
    return custom_task

# Task execution configurations
TASK_CONFIGURATIONS = {
    "comprehensive": {
        "max_execution_time": 1800,  # 30 minutes
        "retry_attempts": 3,
        "parallel_execution": False
    },
    "quick": {
        "max_execution_time": 600,  # 10 minutes
        "retry_attempts": 2,
        "parallel_execution": True
    },
    "risk_focused": {
        "max_execution_time": 1200,  # 20 minutes
        "retry_attempts": 3,
        "parallel_execution": False
    },
    "esg_focused": {
        "max_execution_time": 900,  # 15 minutes
        "retry_attempts": 2,
        "parallel_execution": False
    }
}

# Export key functions and configurations
__all__ = [
    'define_tasks',
    'create_custom_task',
    'TaskManager',
    'TASK_CONFIGURATIONS',
    'create_output_template'
]