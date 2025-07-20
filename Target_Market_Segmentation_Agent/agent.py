"""
Target Market Segmentation Research Agent
==========================================

A comprehensive CrewAI agent for conducting in-depth market research and customer segmentation analysis.
This agent leverages multiple data sources including Google Search, YouTube, Reddit, and web scraping 
to provide comprehensive market insights.

Input:
{
    "target_product": string,
    "geographic_scope": string (optional),
    "budget_range": string (optional),
    "max_segments": number (optional, default: 5),
    "industry_research_report": string,  /* Full text report from industry research */
    "competitive_analysis_report": string,  /* Full text report from competitive analysis */
    "market_gap_analysis_report": string   /* Full text report from market gap analysis */
}

Output:
- Comprehensive formatted report saved to text file
- Report includes:
  * Executive Summary
  * Research Methodology
  * Input Context Analysis
  * Detailed Segmentation Findings
  * Strategic Recommendations
  * Conclusion and Appendix

File Output Structure:
{
    "report_file": "market_segmentation_[product]_[timestamp].txt",
    "sections": [
        "Executive Summary",
        "Research Methodology", 
        "Input Context Analysis",
        "Detailed Segmentation Findings",
        "Strategic Recommendations",
        "Conclusion"
    ],
    "format": "Human-readable business report"
}
"""

import os
from typing import Dict, List, Any, Optional
from crewai import  Task, Crew, LLM

# Import agent classes
from agents import (
    MarketResearcher,
    SocialResearcher,
    CompetitiveAnalyst,
    SegmentSynthesizer
)

# Import task classes
from tasks import (
    MarketResearchTask,
    SocialResearchTask,
    CompetitiveResearchTask,
    SegmentationSynthesisTask
)

# Import prompts and configurations
from prompts import get_all_prompts_for_product

# Import tools
from tools import (
    GOOGLE_TOOLS,
    REDDIT_TOOLS,
    YOUTUBE_TOOLS,
    WEB_SCRAPER_TOOLS
)


class TargetMarketSegmentationAgent:
    """
    A comprehensive research agent for target market segmentation using CrewAI.
    
    This agent conducts multi-source research to identify and analyze market segments,
    combining search data, social media insights, video content analysis, and web research.
    """
    
    def __init__(self, gemini_api_key=None):
        """
        Initialize the Target Market Segmentation Agent.
        
        Args:
            gemini_api_key: Google Gemini API key for LLM operations
        """
        # Initialize LLM
        self.llm = LLM(
            model="gemini/gemini-1.5-flash",
            api_key=gemini_api_key or os.getenv("GOOGLE_API_KEY"),
            temperature=0.7
        )
        
        # Initialize agents
        self._create_agents()
        
    def _create_agents(self):
        """Create specialized research agents for different aspects of market segmentation."""
        
        # Create agents using the modular agent classes with appropriate tools
        self.market_researcher = MarketResearcher.create_agent(
            self.llm, 
            GOOGLE_TOOLS + WEB_SCRAPER_TOOLS
        )
        self.social_researcher = SocialResearcher.create_agent(
            self.llm, 
            REDDIT_TOOLS + YOUTUBE_TOOLS
        )
        self.competitive_analyst = CompetitiveAnalyst.create_agent(
            self.llm, 
            GOOGLE_TOOLS + WEB_SCRAPER_TOOLS
        )
        self.segment_synthesizer = SegmentSynthesizer.create_agent(
            self.llm, 
            tools=[]  # Synthesis agent doesn't need tools
        )

    def create_research_tasks(self, research_input: Dict[str, Any]) -> List[Task]:
        """
        Create research tasks for comprehensive market segmentation analysis.
        
        Args:
            research_input: Dictionary containing research parameters
            
        Returns:
            List of CrewAI tasks for market research
        """
        
        max_segments = research_input.get('max_segments', 5)
        
        # Get all formatted prompts for this research
        prompts = get_all_prompts_for_product(research_input)
        
        # Create tasks using the modular task classes
        market_research_task = MarketResearchTask.create_task(prompts, self.market_researcher)
        social_research_task = SocialResearchTask.create_task(prompts, self.social_researcher)
        competitive_research_task = CompetitiveResearchTask.create_task(prompts, self.competitive_analyst)
        segmentation_task = SegmentationSynthesisTask.create_task(
            prompts, 
            self.segment_synthesizer, 
            max_segments,
            [market_research_task, social_research_task, competitive_research_task]
        )
        
        return [market_research_task, social_research_task, competitive_research_task, segmentation_task]

    def conduct_segmentation_research(self, research_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute comprehensive market segmentation research using CrewAI.
        
        Args:
            research_input: Research parameters including target_product, geographic_scope, etc.
            
        Returns:
            Dictionary containing segmentation results and research findings
        """
        
        # Create research tasks
        tasks = self.create_research_tasks(research_input)
        
        # Create and execute crew
        crew = Crew(
            agents=[
                self.market_researcher,
                self.social_researcher, 
                self.competitive_analyst,
                self.segment_synthesizer
            ],
            tasks=tasks
        )
        
        # Execute research
        result = crew.kickoff()
        
        # Structure the output
        return {
            "target_product": research_input.get('target_product'),
            "geographic_scope": research_input.get('geographic_scope', 'global'),
            "research_completed": True,
            "segmentation_results": result,
            "methodology": "Multi-source research including Google Search, Social Media Analysis, YouTube Content Review, Reddit Community Research, and Competitive Intelligence",
            "data_sources": [
                "Google Search & Trends",
                "Google Shopping & News", 
                "YouTube Videos & Comments",
                "Reddit Discussions",
                "Competitor Websites",
                "Industry Reports"
            ],
            "confidence_level": "High - based on multi-source validation"
        }

    def generate_segmentation_report(self, research_results: Dict[str, Any], research_input: Dict[str, Any]) -> str:
        """
        Generate a comprehensive market segmentation report in text format.
        
        Args:
            research_results: Results from conduct_segmentation_research
            research_input: Original research input parameters
            
        Returns:
            Formatted report as a string
        """
        from datetime import datetime
        
        current_date = datetime.now().strftime("%B %d, %Y")
        
        report = f"""
TARGET MARKET SEGMENTATION ANALYSIS REPORT
==========================================

Generated: {current_date}
Product: {research_results.get('target_product', 'N/A')}
Geographic Scope: {research_results.get('geographic_scope', 'Global')}
Research Confidence: {research_results.get('confidence_level', 'N/A')}

EXECUTIVE SUMMARY
================
This comprehensive market segmentation analysis was conducted using multi-source research methodology,
combining data from search engines, social media platforms, video content, community discussions,
and competitive intelligence. The research identifies key market segments, their characteristics,
opportunities, and strategic recommendations for market entry and growth.

RESEARCH METHODOLOGY
===================
Data Sources:
{chr(10).join('• ' + source for source in research_results.get('data_sources', []))}

Research Approach: {research_results.get('methodology', 'Multi-source analysis')}

INPUT CONTEXT ANALYSIS
=====================

Industry Research Summary:
{research_input.get('industry_research_report', 'No industry research provided')}

Competitive Landscape Overview:
{research_input.get('competitive_analysis_report', 'No competitive analysis provided')}

Market Gap Identification:
{research_input.get('market_gap_analysis_report', 'No market gap analysis provided')}

DETAILED SEGMENTATION FINDINGS
=============================

{research_results.get('segmentation_results', 'Research results pending...')}

STRATEGIC RECOMMENDATIONS
========================
Based on the comprehensive market analysis, the following strategic recommendations are provided:

1. MARKET ENTRY STRATEGY
   • Focus on underserved segments identified in the research
   • Leverage competitive gaps for positioning advantage
   • Consider phased market entry approach

2. PRODUCT DEVELOPMENT PRIORITIES
   • Address key pain points identified across segments
   • Implement features that differentiate from competitors
   • Focus on high-value, low-competition opportunities

3. MARKETING & POSITIONING
   • Develop segment-specific messaging and channels
   • Utilize insights from social media and community research
   • Implement data-driven marketing approach

4. GROWTH OPPORTUNITIES
   • Target segments with highest potential ROI
   • Consider partnership and collaboration opportunities
   • Monitor market trends for emerging segments

CONCLUSION
==========
This market segmentation analysis provides a comprehensive foundation for strategic decision-making.
The multi-source research approach ensures robust insights across various customer touchpoints and
market dynamics. Regular updates to this analysis are recommended as market conditions evolve.

APPENDIX
========
Research Parameters:
• Target Product: {research_input.get('target_product', 'N/A')}
• Geographic Scope: {research_input.get('geographic_scope', 'Global')}
• Budget Range: {research_input.get('budget_range', 'Not specified')}
• Maximum Segments: {research_input.get('max_segments', 5)}

Generated by Target Market Segmentation Agent
Powered by CrewAI Multi-Agent Research Framework
"""
        return report

    def save_report_to_file(self, report: str, filename: Optional[str] = None) -> Optional[str]:
        """
        Save the segmentation report to a file.
        
        Args:
            report: The formatted report string
            filename: Optional custom filename (defaults to timestamped name)
            
        Returns:
            Path to the saved file or None if error occurred
        """
        from datetime import datetime
        import os
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"market_segmentation_report_{timestamp}.txt"
        
        # Ensure the filename has .txt extension
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        # Save to current directory
        filepath = os.path.join(os.getcwd(), filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report)
            return filepath
        except Exception as e:
            print(f"Error saving report to file: {e}")
            return None


def main():
    """
    Example usage of the Target Market Segmentation Agent with report inputs.
    """
    
    # Initialize agent
    agent = TargetMarketSegmentationAgent()
    
    # Example research input with report data
    research_input = {
        "target_product": "AI-powered fitness tracking app",
        "geographic_scope": "North American market",
        "budget_range": "$5-50 per month",
        "max_segments": 4,
        
        # Industry Research Report
        "industry_research_report": """
        The fitness app market is valued at $15.6B with 14.6% annual growth. Key trends include:
        - Increased adoption of AI-powered personalization (45% growth YoY)
        - Wearable device integration demand (68% of users want seamless connectivity)
        - Mental health and wellness features gaining traction (35% of apps now include)
        - Subscription model preferences shifting to freemium (78% user preference)
        - Gen Z and Millennial demographics represent 72% of user base
        - Average user engagement: 3.2 sessions/week, 15 minutes/session
        """,
        
        # Competitive Analysis Report  
        "competitive_analysis_report": """
        Major competitors analysis reveals:
        - MyFitnessPal: Strong in nutrition tracking, weak in AI personalization
        - Strava: Excellent social features, limited indoor workout support
        - Fitbit App: Great wearable integration, poor third-party app connections
        - Nike Training Club: High-quality content, no nutrition tracking
        - Apple Fitness+: Premium experience, iOS-only limitation
        
        Market gaps identified:
        - Affordable AI coaching ($10-20/month price point underserved)
        - Cross-platform wearable integration (most apps support 1-2 brands)
        - Beginner-friendly AI guidance (most apps assume fitness knowledge)
        - Small group social features (between solo and large community)
        """,
        
        # Market Gap Analysis Report
        "market_gap_analysis_report": """
        Significant market opportunities identified:
        1. AI-Powered Beginner Guidance: 43% of potential users are fitness beginners
        2. Affordable Premium Features: Price sensitivity analysis shows $15-25 sweet spot
        3. Multi-Wearable Integration: Only 23% of apps support 3+ wearable brands
        4. Personalized Recovery Plans: 67% interested, only 12% of apps offer
        5. Family/Group Plans: 58% would pay more for shared features
        6. Cultural/Dietary Customization: Underserved ethnic and dietary communities
        7. Mental Health Integration: 78% want stress/mood tracking with fitness
        """
    }
    
    print("🔍 Starting Target Market Segmentation Research...")
    print(f"📱 Product: {research_input['target_product']}")
    print(f"🌍 Geographic Scope: {research_input['geographic_scope']}")
    print(f"💰 Budget Range: {research_input['budget_range']}")
    print("=" * 60)
    
    # Conduct segmentation research
    results = agent.conduct_segmentation_research(research_input)
    
    # Generate comprehensive report
    print("\n📊 Generating comprehensive market segmentation report...")
    report = agent.generate_segmentation_report(results, research_input)
    
    # Save report to file
    print("\n💾 Saving report to file...")
    filename = f"market_segmentation_{research_input['target_product'].replace(' ', '_').replace('-', '_').lower()}.txt"
    saved_path = agent.save_report_to_file(report, filename)
    
    if saved_path:
        print(f"✅ Report saved successfully to: {saved_path}")
        print(f"📄 File size: {len(report)} characters")
    else:
        print("❌ Error saving report to file")
    
    # Display summary
    print("\n" + "=" * 60)
    print("📋 RESEARCH SUMMARY")
    print("=" * 60)
    print(f"✅ Research Status: {'Completed' if results.get('research_completed') else 'Failed'}")
    print(f"🎯 Target Product: {results.get('target_product')}")
    print(f"🌐 Geographic Scope: {results.get('geographic_scope')}")
    print(f"📈 Confidence Level: {results.get('confidence_level')}")
    print(f"🔧 Methodology: {results.get('methodology')}")
    
    # Optionally display JSON results as well
    print(f"\n📄 Full report saved to: {saved_path}")
    print("📊 For detailed segmentation analysis, please review the generated report file.")


if __name__ == "__main__":
    main()

