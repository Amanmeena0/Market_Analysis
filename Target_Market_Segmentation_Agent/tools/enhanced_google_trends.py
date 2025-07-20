"""
Enhanced Google Trends Tool
===========================

This provides an enhanced Google Trends search that automatically handles
data type selection and provides comprehensive market analysis.
"""

from crewai.tools import tool
from serpapi import GoogleSearch
from .config import serper_api_key, logger


@tool("SmartGoogleTrendsTool")
def smart_search_google_trends(query: str, time: str = "today 12-m", geo: str = "US") -> str:
    """
    Intelligent Google Trends search that automatically selects the best data type
    and combines multiple analysis types for comprehensive market insights.
    
    Args:
        query (str): The search term to analyze
        time (str): Time frame (default: "today 12-m")
        geo (str): Geographic location (default: "US")
        
    Returns:
        str: Comprehensive trends analysis combining multiple data types
    """
    try:
        if not serper_api_key:
            return "Error: SERPER_API_KEY not found in environment variables"
        
        combined_analysis = f"Comprehensive Google Trends Analysis for '{query}' in {geo} ({time}):\n\n"
        
        # 1. Get TIMESERIES data (works with single queries)
        timeseries_result = _get_trends_data(query, time, geo, "TIMESERIES")
        if timeseries_result:
            combined_analysis += "TREND TIMELINE ANALYSIS:\n"
            combined_analysis += timeseries_result + "\n\n"
        
        # 2. Get RELATED_QUERIES data (works best with single queries)
        related_result = _get_trends_data(query, time, geo, "RELATED_QUERIES")
        if related_result:
            combined_analysis += "RELATED SEARCH ANALYSIS:\n"
            combined_analysis += related_result + "\n\n"
        
        # 3. Add market insights
        combined_analysis += _generate_market_insights(query, geo)
        
        return combined_analysis
        
    except Exception as e:
        logger.error(f"Error in smart_search_google_trends: {e}")
        return f"Error in comprehensive trends analysis: {str(e)}"


def _get_trends_data(query: str, time: str, geo: str, data_type: str) -> str:
    """Helper function to get specific trends data type."""
    try:
        params = {
            "engine": "google_trends",
            "q": query,
            "hl": "en",
            "api_key": serper_api_key,
            "data_type": data_type,
            "time": time,
            "geo": geo,
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        if "error" in results:
            logger.warning(f"SerpApi Error for {data_type}: {results['error']}")
            return ""

        analysis = ""
        
        if data_type == "TIMESERIES" and "interest_over_time" in results:
            timeline_data = results["interest_over_time"]["timeline_data"]
            if timeline_data:
                # Process timeline data safely
                recent_values = []
                all_values = []
                
                for item in timeline_data:
                    if 'values' in item and len(item['values']) > 0:
                        value = item['values'][0].get('value', 0)
                        try:
                            numeric_value = int(value) if value is not None else 0
                            all_values.append(numeric_value)
                            if len(all_values) > len(timeline_data) - 5:
                                recent_values.append(numeric_value)
                        except (ValueError, TypeError):
                            continue
                
                if recent_values and all_values:
                    avg_recent = sum(recent_values) / len(recent_values)
                    peak_interest = max(all_values)
                    
                    analysis += f"• Average recent interest: {avg_recent:.1f}\n"
                    analysis += f"• Peak interest level: {peak_interest}\n"
                    analysis += f"• Current trend: {'Rising' if len(recent_values) > 1 and recent_values[-1] > recent_values[0] else 'Declining'}\n"
        
        elif data_type == "RELATED_QUERIES" and "related_queries" in results:
            rising = results["related_queries"].get("rising", [])
            top = results["related_queries"].get("top", [])
            
            if rising:
                rising_queries = [str(q.get('query', '')) for q in rising[:5] if q.get('query')]
                if rising_queries:
                    analysis += f"• Rising searches: {', '.join(rising_queries)}\n"
            
            if top:
                top_queries = [str(q.get('query', '')) for q in top[:5] if q.get('query')]
                if top_queries:
                    analysis += f"• Top related searches: {', '.join(top_queries)}\n"
        
        return analysis
        
    except Exception as e:
        logger.warning(f"Error getting {data_type} data: {e}")
        return ""


def _generate_market_insights(query: str, geo: str) -> str:
    """Generate market insights based on the search query."""
    insights = "MARKET INSIGHTS:\n"
    
    # Basic market analysis based on query type
    query_lower = query.lower()
    
    if 'app' in query_lower:
        insights += "• Mobile app market analysis recommended\n"
        insights += "• Consider app store trends and user reviews\n"
    
    if 'fitness' in query_lower or 'health' in query_lower:
        insights += "• Health & wellness market segment\n"
        insights += "• Consider seasonal trends (New Year, summer)\n"
    
    if 'ai' in query_lower or 'artificial intelligence' in query_lower:
        insights += "• Technology adoption trends important\n"
        insights += "• B2B vs B2C market differentiation needed\n"
    
    insights += f"• Geographic focus: {geo} market\n"
    insights += "• Recommend cross-referencing with competitor analysis\n"
    
    return insights
