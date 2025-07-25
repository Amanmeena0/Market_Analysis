from crewai import Agent, Task


barrier_assessment_agent = Agent(
    role="Barrier Assessment Specialist",
    goal="Analyze startup costs, legal/regulatory hurdles, and incumbent advertising spend to identify market entry barriers and recommend mitigation strategies",
    backstory="You are an experienced market research analyst specializing in barrier assessment and market entry strategies. You have deep expertise in financial analysis, regulatory compliance, competitive intelligence, and strategic partnerships. You excel at identifying potential obstacles to market success and developing actionable mitigation strategies including partnerships, licensing agreements, and lean MVP approaches.",
)

barrier_assessment_task = Task(
    description="Conduct a comprehensive barrier assessment focusing on startup costs analysis, legal and regulatory hurdles evaluation, and incumbent advertising spend research. Analyze financial requirements for market entry, identify regulatory compliance challenges, and assess competitive advertising investments. Develop strategic recommendations for overcoming these barriers through partnerships, licensing agreements, and lean MVP approaches.",
    agent=barrier_assessment_agent,
    expected_output="A detailed barrier assessment report including: startup cost breakdown and financial requirements analysis, comprehensive review of legal and regulatory hurdles with compliance requirements, analysis of incumbent advertising spend and competitive investment levels, and strategic mitigation recommendations such as partnership opportunities, licensing strategies, and lean MVP implementation plans.",
)
