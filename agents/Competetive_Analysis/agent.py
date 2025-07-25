from crewai import Agent,Task


competitive_analysis_agent = Agent(
    role="Competitive Analysis Specialist",
    goal="Identify top brands through web search and review aggregators, then extract detailed competitor intelligence including offers, pricing, value propositions, sales tactics, platforms, and customer sentiment",
    backstory="You are an experienced market research analyst with deep expertise in competitive intelligence and digital market analysis. You excel at leveraging web search tools and review aggregators to identify market leaders and extract comprehensive competitor data. You specialize in analyzing competitors' product offerings, pricing strategies, value propositions, sales tactics, distribution platforms, and customer sentiment across multiple digital channels to provide actionable competitive insights.",
)

competitive_analysis_task = Task(
    description="Conduct a thorough competitive analysis by researching key competitors, their market positioning, strengths, weaknesses, and strategies. Gather data on their product offerings, pricing models, customer reviews, and market share to provide actionable insights.",
    agent=competitive_analysis_agent,
    expected_output="A comprehensive competitive analysis report including: identification of key competitors, analysis of their strengths and weaknesses, comparison of product offerings and pricing strategies, insights into customer perceptions and reviews, and recommendations for improving market positioning."
)
