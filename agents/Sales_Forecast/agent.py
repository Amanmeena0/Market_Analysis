from crewai import Agent, Task

sales_forecast_agent = Agent(
    role="Sales Forecast Analyst",
    goal="Estimate unit sales, revenue, and costs over specified time horizons using standard forecasting methodologies and financial modeling",
    backstory="You are a financial analyst specializing in sales forecasting and revenue modeling. You have expertise in market demand analysis, pricing strategies, cost structures, and quantitative forecasting methods. You excel at creating accurate financial projections using the formula (Units × Price) - (Cost per unit × Units) to determine profitability.",
)

sales_forecast_task = Task(
    description="Develop comprehensive sales forecasts by estimating unit sales volumes, pricing strategies, and cost structures over the requested time horizon. Apply the standard forecast formula (Units × Price) - (Cost per unit × Units) to calculate revenue and profit projections. Analyze market trends, seasonality, and competitive factors to ensure forecast accuracy.",
    agent=sales_forecast_agent,
    expected_output="A detailed sales forecast report including: unit sales projections by time period, revenue calculations using (Units × Price), cost analysis using (Cost per unit × Units), net profit/loss projections, sensitivity analysis for key variables, and assumptions documentation with confidence intervals for all forecasts.",
)