"""
Target Market Segmentation Agent Tools
=====================================

A comprehensive toolkit for market research and analysis including:
- Google Search, Trends, Shopping, and News tools
- YouTube content and sentiment analysis tools  
- Reddit community research and sentiment tools
- Web scraping and content analysis tools

Usage:
    from tools import (
        search_google, search_google_trends, search_google_shopping, search_google_news,
        search_youtube, get_youtube_comments, summarize_youtube_transcript,
        get_reddit_post_data, find_relevant_subreddits,
        scrape_website_to_markdown, analyze_web_content, scrape_multiple_urls
    )
"""

# Import all tools from their respective modules
from .google_tools import (
    search_google,
    search_google_trends, 
    search_google_shopping,
    search_google_news
)

# Import enhanced tools
from .enhanced_google_trends import (
    smart_search_google_trends
)

from .youtube_tools import (
    search_youtube,
    get_youtube_comments,
    summarize_youtube_transcript
)

from .reddit_tools import (
    get_reddit_post_data,
    find_relevant_subreddits
)

from .web_scraper_tools import (
    scrape_website_to_markdown,
)

# Export all tools for easy importing
__all__ = [
    # Google Tools
    'search_google',
    'search_google_trends',
    'search_google_shopping', 
    'search_google_news',
    
    # Enhanced Tools
    'smart_search_google_trends',
    
    # YouTube Tools
    'search_youtube',
    'get_youtube_comments',
    'summarize_youtube_transcript',
    
    # Reddit Tools
    'get_reddit_post_data',
    'find_relevant_subreddits',
    
    # Web Scraper Tools
    'scrape_website_to_markdown',
    
]

# Tool categories for organized access
GOOGLE_TOOLS = [
    search_google,
    search_google_trends,
    search_google_shopping,
    search_google_news,
    smart_search_google_trends  # Enhanced trends tool
]

YOUTUBE_TOOLS = [
    search_youtube,
    get_youtube_comments,
    summarize_youtube_transcript
]

REDDIT_TOOLS = [
    get_reddit_post_data,
    find_relevant_subreddits
]

WEB_SCRAPER_TOOLS = [
    scrape_website_to_markdown,
]

ALL_TOOLS = GOOGLE_TOOLS + YOUTUBE_TOOLS + REDDIT_TOOLS + WEB_SCRAPER_TOOLS
