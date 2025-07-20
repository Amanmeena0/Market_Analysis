"""
Google Search related tools for market research
"""
from crewai.tools import tool
from serpapi import GoogleSearch
from .config import serper_api_key, logger


@tool("GoogleSearchTool")
def search_google(query: str) -> str:
    """
    Search Google for information on a specific query and return a comprehensive summary.
    
    Args:
        query (str): The search query to look for
        
    Returns:
        str: Comprehensive summary of search results with key insights and sources
    """
    try:
        if not serper_api_key:
            return "Error: SERPER_API_KEY not found in environment variables"
            
        params = {
            "q": query,
            "hl": "en",
            "gl": "us",
            "api_key": serper_api_key
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        
        if 'organic_results' not in results:
            return "No search results found"
        
        # Create a comprehensive summary
        summary = f"Search Results for '{query}':\n\n"
        
        for i, result in enumerate(results['organic_results'][:5], 1):
            title = result.get('title', 'No title')
            snippet = result.get('snippet', 'No description')
            source = result.get('source', 'Unknown source')
            link = result.get('link', '')
            
            summary += f"{i}. {title}\n"
            summary += f"   Source: {source}\n"
            summary += f"   Summary: {snippet}\n"
            summary += f"   Link: {link}\n\n"
        
        # Add key insights
        summary += "Key Insights:\n"
        summary += f"- Found {len(results.get('organic_results', []))} relevant results\n"
        summary += f"- Top sources include: {', '.join([r.get('source', '') for r in results['organic_results']])}\n"
        
        return summary
    except Exception as e:
        logger.error(f"Error in search_google: {e}")
        return f"Error searching Google: {str(e)}"


@tool("GoogleTrendsTool")
def search_google_trends(query: str, time: str = "today 12-m", geo: str = "US", data_type: str = "TIMESERIES") -> str:
    """
    Fetch Google Trends data for market analysis and trend identification.
    
    Args:
        query (str): The search term or comma-separated terms to get trends for
        time (str): Time frame (default: "today 12-m"). Examples: "now 7-d", "today 3-m"
        geo (str): Geographic location as country code (default: "US" for United States)
        data_type (str): Type of data ("TIMESERIES", "RELATED_QUERIES") - GEO_MAP requires multiple queries
        
    Returns:
        str: Comprehensive analysis of trends data with market insights
    """
    try:
        if not serper_api_key:
            return "Error: SERPER_API_KEY not found in environment variables"
        
        # Validate and adjust data_type based on query format
        query_count = len([q.strip() for q in query.split(',') if q.strip()])
        
        # GEO_MAP requires multiple queries, so fallback to TIMESERIES for single queries
        if data_type == "GEO_MAP" and query_count == 1:
            data_type = "TIMESERIES"
            print(f"Note: Changed data_type from GEO_MAP to TIMESERIES for single query compatibility")
        
        # RELATED_QUERIES works best with single queries
        if data_type == "RELATED_QUERIES" and query_count > 1:
            # Take only the first query for related queries
            query = query.split(',')[0].strip()
            print(f"Note: Using first query '{query}' for RELATED_QUERIES analysis")
            
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
            return f"SerpApi Error: {results['error']}"

        # Create a comprehensive trends analysis
        analysis = f"Google Trends Analysis for '{query}' in {geo} ({time}):\n\n"
        
        if data_type == "TIMESERIES" and "interest_over_time" in results:
            timeline_data = results["interest_over_time"]["timeline_data"]
            if timeline_data:
                # Get recent trend values
                recent_values = [item["values"][0]["value"] for item in timeline_data[-5:]]
                avg_recent = sum(recent_values) / len(recent_values)
                
                analysis += f"Trend Analysis:\n"
                analysis += f"- Average recent interest: {avg_recent}\n"
                analysis += f"- Peak interest: {max([item['values'][0]['value'] for item in timeline_data])}\n"
                analysis += f"- Current trend: {'Rising' if recent_values[-1] > recent_values[0] else 'Declining'}\n\n"
        
        if "related_queries" in results:
            rising = results["related_queries"].get("rising", [])
            top = results["related_queries"].get("top", [])
            
            analysis += "Related Trends:\n"
            if rising:
                analysis += f"- Rising queries: {', '.join([q['query'] for q in rising[:5]])}\n"
            if top:
                analysis += f"- Top queries: {', '.join([q['query'] for q in top[:5]])}\n"
        
        return analysis
    except Exception as e:
        logger.error(f"Error in search_google_trends: {e}")
        return f"Error fetching Google Trends: {str(e)}"


@tool("GoogleShoppingTool")
def search_google_shopping(query: str, sort_by: str = 'relevance', min_price = None, max_price  = None, condition = None, location = None, num_results: int = 10) -> str:
    """
    Search Google Shopping for products with comprehensive filtering options.
    
    Args:
        query (str): The product or term to search for
        sort_by (str): Sorting order ('relevance', 'price_low_to_high', 'price_high_to_low', 'rating')
        min_price (float): Minimum price filter
        max_price (float): Maximum price filter
        condition (str): Product condition ('new', 'used')
        location (str): Location for search
        num_results (int): Number of results to return (default: 10)
        
    Returns:
        str: Market analysis summary of product pricing and availability
    """
    try:
        if not serper_api_key:
            return "Error: SERPER_API_KEY not found in environment variables"
            
        params = {
            "engine": "google_shopping",
            "q": query,
            "api_key": serper_api_key,
            "num": num_results,
        }

        if location:
            params["location"] = location

        tbs_params = []
        sort_map = {
            'relevance': 'p_ord:rv',
            'price_low_to_high': 'p_ord:p',
            'price_high_to_low': 'p_ord:pd',
            'rating': 'p_ord:r'
        }
        if sort_by and sort_by in sort_map:
            tbs_params.append(sort_map[sort_by])

        if min_price is not None or max_price is not None:
            tbs_params.append('price:1')
            if min_price is not None:
                tbs_params.append(f'ppr_min:{min_price}')
            if max_price is not None:
                tbs_params.append(f'ppr_max:{max_price}')

        condition_map = {'new': 'cond:c', 'used': 'cond:u'}
        if condition and condition in condition_map:
            tbs_params.append(condition_map[condition])

        if tbs_params:
            params['tbs'] = ",".join(tbs_params)

        search = GoogleSearch(params)
        results = search.get_dict()

        if "error" in results:
            return f"SerpApi Error: {results['error']}"

        # Create market analysis summary
        if 'shopping_results' not in results:
            return f"No shopping results found for '{query}'"
        
        shopping_data = results['shopping_results']
        analysis = f"Market Analysis for '{query}':\n\n"
        
        # Price analysis
        prices = []
        top_sellers = []
        
        for item in shopping_data[:10]:
            if 'price' in item:
                price_str = item['price'].replace('$', '').replace(',', '')
                try:
                    price = float(price_str)
                    prices.append(price)
                except:
                    pass
            
            if 'source' in item:
                top_sellers.append(item['source'])
        
        if prices:
            analysis += f"Price Analysis:\n"
            analysis += f"- Price range: ${min(prices):.2f} - ${max(prices):.2f}\n"
            analysis += f"- Average price: ${sum(prices)/len(prices):.2f}\n"
            analysis += f"- Total products analyzed: {len(shopping_data)}\n\n"
        
        if top_sellers:
            unique_sellers = list(set(top_sellers))
            analysis += f"Top Sellers: {', '.join(unique_sellers[:5])}\n\n"
        
        # Product highlights
        analysis += "Product Highlights:\n"
        for i, item in enumerate(shopping_data[:3], 1):
            title = item.get('title', 'No title')
            price = item.get('price', 'Price not available')
            rating = item.get('rating', 'No rating')
            
            analysis += f"{i}. {title}\n"
            analysis += f"   Price: {price} | Rating: {rating}\n"
        
        return analysis
    except Exception as e:
        logger.error(f"Error in search_google_shopping: {e}")
        return f"Error searching Google Shopping: {str(e)}"


@tool("GoogleNewsTool")
def search_google_news(query: str, location  = None, sort_by  = None, time_period  = None, num_results: int = 10) -> str:
    """
    Search Google News for recent articles and news coverage.
    
    Args:
        query (str): The topic or keyword to search for
        location (str): Location for the search
        sort_by (str): Sorting order ('relevance' or 'date')
        time_period (str): Time frame ('past_hour', 'past_day', 'past_week', 'past_month', 'past_year')
        num_results (int): Number of articles to return (default: 10)
        
    Returns:
        str: Comprehensive news analysis with sentiment and coverage summary
    """
    try:
        if not serper_api_key:
            return "Error: SERPER_API_KEY not found in environment variables"
            
        params = {
            "engine": "google",
            "tbm": "nws",
            "q": query,
            "api_key": serper_api_key,
            "num": num_results,
        }
        
        if location:
            params["location"] = location

        tbs_params = []
        if sort_by == 'date':
            tbs_params.append("sbd:1")

        time_map = {
            'past_hour': 'qdr:h', 'past_day': 'qdr:d', 'past_week': 'qdr:w',
            'past_month': 'qdr:m', 'past_year': 'qdr:y'
        }
        if time_period in time_map:
            tbs_params.append(time_map[time_period])

        if tbs_params:
            params["tbs"] = ",".join(tbs_params)

        search = GoogleSearch(params)
        results = search.get_dict()
        
        if 'news_results' not in results:
            return f"No news results found for '{query}'"
        
        news_data = results['news_results']
        analysis = f"News Coverage Analysis for '{query}':\n\n"
        
        # Coverage summary
        analysis += f"Media Coverage Summary:\n"
        analysis += f"- Total articles found: {len(news_data)}\n"
        analysis += f"- Time period: {time_period or 'All time'}\n"
        analysis += f"- Search location: {location or 'Global'}\n\n"
        
        # Key headlines
        analysis += "Key Headlines:\n"
        for i, article in enumerate(news_data, 1):
            title = article.get('title', 'No title')
            source = article.get('source', 'Unknown source')
            date = article.get('date', 'No date')
            snippet = article.get('snippet', '')
            
            analysis += f"{i}. {title}\n"
            analysis += f"   Source: {source} | Date: {date}\n"
            if snippet:
                analysis += f"   Summary: {snippet}...\n"
            analysis += "\n"
        
        # Source analysis
        sources = [article.get('source', '') for article in news_data if article.get('source')]
        unique_sources = list(set(sources))
        analysis += f"Coverage Sources: {', '.join(unique_sources[:10])}\n"
        
        return analysis
    except Exception as e:
        logger.error(f"Error in search_google_news: {e}")
        return f"Error searching Google News: {str(e)}"
