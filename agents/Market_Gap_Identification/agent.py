from crewai import Agent, Task

market_gap_agent = Agent(
    role="Market Gap Identification Specialist",
    goal="Compare industry data with competitor coverage, highlight unmet needs and areas of low competition, and analyze consumer feedback to identify market opportunities",
    backstory="You are a strategic market research analyst with expertise in competitive intelligence, gap analysis, and consumer behavior research. You excel at identifying underserved market segments, analyzing competitor positioning, and interpreting consumer sentiment data to uncover hidden opportunities in the marketplace.",
)

market_gap_task = Task(
    description="Conduct comprehensive market gap analysis by comparing industry data against competitor coverage maps, identifying unmet consumer needs and low-competition areas. Analyze consumer feedback through surveys and sentiment mining to validate opportunity areas. Create actionable insights for market entry in underserved segments.",
    agent=market_gap_agent,
    expected_output="A comprehensive market gap analysis report including: industry vs competitor coverage comparison matrix, identification of unmet needs and underserved segments, competitive intensity mapping by market area, consumer sentiment analysis and feedback synthesis, and prioritized market opportunity recommendations with entry strategies.",
)