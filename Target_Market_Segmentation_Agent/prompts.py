from typing import Dict, Any

class AgentPrompts:
    """Container class for all agent prompts and task descriptions."""
    
    @staticmethod
    def get_market_research_task_description(target_product: str, geographic_scope: str, budget_range: str) -> str:
        """
        Get the task description for the primary market research agent.
        
        Args:
            target_product: The product/service being researched
            geographic_scope: Geographic market scope
            budget_range: Price range or budget constraints
            
        Returns:
            Formatted task description string
        """
        return f"""
        Conduct comprehensive primary market research for {target_product} in the {geographic_scope}.
        
        Your research should include:
        1. Market size and growth trends analysis
        2. Customer demographic patterns and preferences  
        3. Current market trends and emerging opportunities
        4. Price sensitivity and purchasing behavior patterns
        5. Geographic and regional market variations
        6. Seasonal or cyclical market patterns
        
        Use Google Search, Google Trends, Google Shopping, and Google News to gather:
        - Market size estimates and industry reports
        - Consumer behavior studies and surveys
        - Industry news and trend analysis
        - Pricing information and competitive landscape
        - Regional market differences and opportunities
        
        Focus on finding data that will help identify distinct customer groups with different:
        - Demographics (age, income, location, etc.)
        - Needs and pain points
        - Purchasing behaviors and preferences
        - Price sensitivity levels
        - Channel preferences
        
        Provide detailed findings with specific data points and sources.
        """

    @staticmethod
    def get_social_research_task_description(target_product: str) -> str:
        """
        Get the task description for the social media research agent.
        
        Args:
            target_product: The product/service being researched
            
        Returns:
            Formatted task description string
        """
        return f"""
        Analyze social media conversations and community discussions about {target_product} to understand:
        
        1. Customer sentiments and opinions
        2. Common pain points and complaints
        3. Desired features and improvements
        4. User personas and behavioral patterns
        5. Community-driven trends and preferences
        6. Influencer opinions and recommendations
        
        Research approach:
        - Search YouTube for product reviews, tutorials, and user experiences
        - Analyze YouTube comments for sentiment and common themes
        - Find relevant Reddit communities discussing the product category
        - Analyze Reddit discussions for authentic customer feedback
        - Identify different user types based on their online behavior
        
        Pay special attention to:
        - Different use cases and user scenarios
        - Varying levels of expertise (beginners vs experts)
        - Different motivations for purchase/use
        - Geographic or cultural differences in usage
        - Age or demographic-related preferences
        
        Organize findings by distinct user groups or behavioral patterns.
        """

    @staticmethod
    def get_competitive_research_task_description(target_product: str) -> str:
        """
        Get the task description for the competitive intelligence agent.
        
        Args:
            target_product: The product/service being researched
            
        Returns:
            Formatted task description string
        """
        return f"""
        Conduct competitive intelligence research for {target_product} to identify market gaps and positioning opportunities.
        
        Research objectives:
        1. Identify key competitors and their target segments
        2. Analyze competitor pricing strategies and positioning
        3. Map competitor strengths and weaknesses
        4. Identify underserved market segments
        5. Find differentiation opportunities
        6. Analyze competitor customer reviews and feedback
        
        Research methodology:
        - Search for competitor websites and analyze their positioning
        - Research competitor pricing and product offerings
        - Analyze competitor customer reviews and ratings
        - Identify gaps in competitor offerings
        - Map competitor target audiences and messaging
        
        Focus on finding:
        - Segments competitors are NOT targeting effectively
        - Price points with limited competition
        - Feature gaps in competitor products
        - Customer complaints about existing solutions
        - Opportunities for better customer experience
        
        Organize findings to highlight market opportunities and gaps.
        """

    @staticmethod
    def get_segmentation_synthesis_task_description(target_product: str, max_segments: int) -> str:
        """
        Get the task description for the market segmentation synthesizer agent.
        
        Args:
            target_product: The product/service being researched
            max_segments: Maximum number of segments to create
            
        Returns:
            Formatted task description string
        """
        return f"""
        Synthesize all research findings to create {max_segments} distinct market segments for {target_product}.
        
        Using the research from the market research, social media analysis, and competitive intelligence tasks, create a comprehensive segmentation framework.
        
        For each market segment, provide:
        
        1. **Segment Profile:**
           - Segment name and clear description
           - Size estimate and growth potential
           - Geographic distribution
           
        2. **Demographics:**
           - Age range, income level, education
           - Occupation, family status
           - Geographic location preferences
           
        3. **Psychographics:**
           - Values, attitudes, lifestyle
           - Motivations and goals
           - Technology adoption level
           - Brand preferences and loyalty
           
        4. **Behavioral Characteristics:**
           - Purchase decision process
           - Price sensitivity and budget
           - Channel preferences (online/offline)
           - Usage patterns and frequency
           
        5. **Pain Points & Needs:**
           - Primary problems they're trying to solve
           - Unmet needs and frustrations
           - Decision-making challenges
           
        6. **Opportunities:**
           - How to reach this segment effectively
           - Messaging that resonates
           - Product/service improvements needed
           - Pricing strategy recommendations
           
        7. **Evidence & Sources:**
           - Specific data supporting this segment's existence
           - Research sources and citations
           - Confidence level in segment viability
        
        Ensure segments are:
        - Mutually exclusive and collectively exhaustive
        - Actionable and reachable
        - Substantial enough to be profitable
        - Distinct in their needs and behaviors
        
        Prioritize segments by attractiveness and strategic fit.
        """


class AgentBackstories:
    """Container class for all agent backstories and role definitions."""
    
    @staticmethod
    def get_market_researcher_backstory() -> str:
        """Get backstory for the market research agent."""
        return """You are a seasoned market research analyst with 15+ years of experience in customer 
        segmentation and market analysis. You excel at synthesizing data from multiple sources to uncover 
        hidden market segments and opportunities. Your expertise spans demographic analysis, psychographic 
        profiling, and behavioral pattern recognition."""

    @staticmethod
    def get_social_researcher_backstory() -> str:
        """Get backstory for the social media research agent."""
        return """You are a digital anthropologist and social media research expert who specializes in 
        understanding online communities and digital behaviors. You can decode social signals, identify 
        emerging trends, and understand the voice of the customer through social platforms."""

    @staticmethod
    def get_competitive_analyst_backstory() -> str:
        """Get backstory for the competitive intelligence agent."""
        return """You are a competitive intelligence expert with deep experience in analyzing competitor 
        strategies and market positioning. You excel at identifying market gaps, pricing opportunities, 
        and differentiation strategies through systematic competitive analysis."""

    @staticmethod
    def get_segment_synthesizer_backstory() -> str:
        """Get backstory for the market segmentation synthesizer agent."""
        return """You are a strategic marketing consultant and segmentation expert who specializes in 
        transforming raw market research into actionable customer segments. You excel at creating data-driven 
        segmentation frameworks that drive business growth and marketing effectiveness."""


class AgentRoles:
    """Container class for all agent roles and goals."""
    
    # Agent Roles
    MARKET_RESEARCHER_ROLE = 'Senior Market Research Analyst'
    SOCIAL_RESEARCHER_ROLE = 'Social Media & Community Research Specialist'
    COMPETITIVE_ANALYST_ROLE = 'Competitive Intelligence Analyst'
    SEGMENT_SYNTHESIZER_ROLE = 'Market Segmentation Strategy Expert'
    
    # Agent Goals
    MARKET_RESEARCHER_GOAL = 'Conduct comprehensive market research to identify distinct customer segments and market opportunities'
    SOCIAL_RESEARCHER_GOAL = 'Analyze social media conversations, community discussions, and user-generated content to understand customer sentiments and behaviors'
    COMPETITIVE_ANALYST_GOAL = 'Research competitor strategies, pricing models, and market positioning to identify gaps and opportunities'
    SEGMENT_SYNTHESIZER_GOAL = 'Synthesize all research findings into actionable market segments with clear targeting strategies'


class TaskOutputs:
    """Container class for expected task outputs."""
    
    MARKET_RESEARCH_OUTPUT = "Comprehensive market research report with demographic data, trends, pricing analysis, and customer behavior insights with specific data points and sources."
    
    SOCIAL_RESEARCH_OUTPUT = "Detailed social media research report identifying distinct user groups, their characteristics, pain points, preferences, and behavioral patterns with supporting evidence from social platforms."
    
    COMPETITIVE_RESEARCH_OUTPUT = "Competitive intelligence report identifying market gaps, competitor weaknesses, underserved segments, and specific opportunities for differentiation."
    
    @staticmethod
    def get_segmentation_output(max_segments: int) -> str:
        """Get expected output for segmentation synthesis task."""
        return f"Complete market segmentation framework with {max_segments} detailed customer segments, each including demographics, psychographics, behaviors, pain points, opportunities, and supporting evidence."


class PromptTemplates:
    """Container class for reusable prompt templates."""
    
    @staticmethod
    def format_research_context(research_input: Dict[str, Any]) -> str:
        """
        Format research context from input parameters including report inputs.
        
        Args:
            research_input: Dictionary containing research parameters and reports
            
        Returns:
            Formatted context string with report information
        """
        context_parts = []
        
        # Add budget considerations
        if research_input.get('budget_range'):
            context_parts.append(f"Budget considerations: {research_input['budget_range']}")
        
        # Add geographic scope
        if research_input.get('geographic_scope'):
            context_parts.append(f"Geographic scope: {research_input['geographic_scope']}")
        
        # Add industry research report
        if research_input.get('industry_research_report'):
            context_parts.append(f"Industry Research Findings:\n{research_input['industry_research_report']}")
        
        # Add competitive analysis report
        if research_input.get('competitive_analysis_report'):
            context_parts.append(f"Competitive Analysis Findings:\n{research_input['competitive_analysis_report']}")
        
        # Add market gap analysis report
        if research_input.get('market_gap_analysis_report'):
            context_parts.append(f"Market Gap Analysis Findings:\n{research_input['market_gap_analysis_report']}")
        
        return '\n\n'.join(context_parts) if context_parts else ""

    @staticmethod
    def add_context_to_description(base_description: str, context: str) -> str:
        """
        Add context information to a task description.
        
        Args:
            base_description: Base task description
            context: Additional context to include
            
        Returns:
            Enhanced task description with context
        """
        if not context:
            return base_description
        
        return f"{base_description}\n\nAdditional Context:\n{context}\n\nConsider this context when conducting your research and analysis."


# Example usage and utility functions
def get_all_prompts_for_product(research_input: Dict[str, Any]) -> Dict[str, str]:
    """
    Get all formatted prompts for a specific product research.
    
    Args:
        research_input: Research parameters
        
    Returns:
        Dictionary containing all formatted prompts
    """
    target_product = research_input.get('target_product', 'the product')
    geographic_scope = research_input.get('geographic_scope', 'global market')
    budget_range = research_input.get('budget_range', 'all price points')
    max_segments = research_input.get('max_segments', 5)
    
    # Get base prompts
    prompts = AgentPrompts()
    context = PromptTemplates.format_research_context(research_input)
    
    return {
        'market_research': PromptTemplates.add_context_to_description(
            prompts.get_market_research_task_description(target_product, geographic_scope, budget_range),
            context
        ),
        'social_research': PromptTemplates.add_context_to_description(
            prompts.get_social_research_task_description(target_product),
            context
        ),
        'competitive_research': PromptTemplates.add_context_to_description(
            prompts.get_competitive_research_task_description(target_product),
            context
        ),
        'segmentation_synthesis': PromptTemplates.add_context_to_description(
            prompts.get_segmentation_synthesis_task_description(target_product, max_segments),
            context
        )
    }
