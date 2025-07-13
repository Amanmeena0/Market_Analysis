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

def define_tasks(company: str, agents=None):
    tasks = []

    # 1. Data Collection Task
    tasks.append(Task(
        description=f"Gather all publicly available data, reports, and datasets about {company}.",
        expected_output="Compiled raw data sources with summaries.",
        tools=[collect_data_sources],
        agent=data_collection_agent
    ))

    # 2. Market Research Task
    tasks.append(Task(
        description=f"Research financial and market data for {company}, including recent news.",
        expected_output="Key financial indicators, market position, and notable events.",
        tools=[get_company_profile, get_latest_news],
        agent=research_agent
    ))

    # 3. Sentiment Analysis Task
    tasks.append(Task(
        description=f"Analyze the sentiment of recent media coverage and investor sentiment for {company}.",
        expected_output="Sentiment summary (positive/negative/neutral) with confidence.",
        tools=[sentiment_analysis],
        agent=sentiment_analysis_agent
    ))

    # 4. Risk Assessment Task
    tasks.append(Task(
        description=f"Identify major risks facing {company} including market, legal, operational, and geopolitical risks.",
        expected_output="Top 3-5 risks with brief impact explanation.",
        tools=[assess_risks],
        agent=risk_assessment_agent
    ))

    # 5. Competitor Analysis Task
    tasks.append(Task(
        description=f"Benchmark {company} against its top competitors in financials, strategy, and innovation.",
        expected_output="Comparison table and strategic positioning insights.",
        tools=[analyze_competitors],
        agent=competitor_analysis_agent
    ))

    # 6. ESG Analysis Task
    tasks.append(Task(
        description=f"Evaluate {company}'s ESG (Environmental, Social, Governance) performance.",
        expected_output="ESG scores, highlights, and red flags if any.",
        tools=[esg_data_fetcher],
        agent=esg_analyst_agent
    ))

    # 7. Macroeconomic Analysis Task
    tasks.append(Task(
        description=f"Analyze macroeconomic indicators affecting {company}'s industry and operations.",
        expected_output="GDP growth, inflation, interest rates, and economic forecast summary.",
        tools=[macroeconomic_data],
        agent=macroeconomic_analyst_agent
    ))

    # 8. Financial Modeling Task
    tasks.append(Task(
        description=f"Model the financial outlook and valuation of {company} using data and analysis.",
        expected_output="DCF model, valuation range, and strategic forecast.",
        tools=[get_latest_news],
        agent=modeling_agent
    ))

    # 9. Report Generation Task
    tasks.append(Task(
        description=f"Write a comprehensive report summarizing all analyses for {company}.",
        expected_output="Structured, visually formatted executive report ready for stakeholders.",
        tools=[get_latest_news],
        agent=report_agent
    ))

    return tasks
