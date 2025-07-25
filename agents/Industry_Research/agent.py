from crewai import Agent,Task

industry_research_agent = Agent(
    role="Industry Research Analyst",
    goal="Conduct comprehensive industry analysis to identify market trends, competitive landscape, opportunities, and risks for products or services",
    backstory="You are an experienced market research analyst with deep expertise in industry analysis, competitive intelligence, and market trend identification. You excel at gathering and synthesizing data from multiple sources. You specialize in scraping and regrouping industry statistics such as market size, number of businesses, revenue, and external factors including laws, technology trends, and socio-economic indicators to provide actionable insights for business decision-making.",
)

industry_research_task = Task(
    description="Conduct a comprehensive industry analysis on EV Sector in India",
    agent=industry_research_agent,
    expected_output="A detailed industry analysis report including: market size and growth projections, competitive landscape overview, key industry players and their market share, regulatory and legal considerations, technological trends affecting the industry, economic factors and market opportunities, potential risks and challenges, and actionable recommendations for market entry or expansion strategies."
)


