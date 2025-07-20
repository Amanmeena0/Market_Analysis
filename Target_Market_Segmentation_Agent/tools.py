"""
Target Market Segmentation Agent Tools - Main Entry Point
=========================================================

This file provides a unified interface to all the modular tools.
The actual tool implementations are now organized in the tools/ directory:

- tools/config.py: Configuration and API initialization
- tools/google_tools.py: Google Search, Trends, Shopping, News tools
- tools/youtube_tools.py: YouTube search, comments, transcript tools  
- tools/reddit_tools.py: Reddit discussion and subreddit analysis tools
- tools/web_scraper_tools.py: Web scraping and content analysis tools

Usage:
    from tools import search_google, search_google_trends, scrape_website_to_markdown, etc.
    
    OR use categorized imports:
    
    from tools import GOOGLE_TOOLS, YOUTUBE_TOOLS, REDDIT_TOOLS, WEB_SCRAPER_TOOLS, ALL_TOOLS
"""

# Import all tools from the modular structure
from tools.google_tools import (
    search_google,
    search_google_trends,
    search_google_shopping,
    search_google_news
)

from tools.enhanced_google_trends import (
    smart_search_google_trends
)

from tools.youtube_tools import (
    search_youtube,
    get_youtube_comments,
    summarize_youtube_transcript
)

from tools.reddit_tools import (
    get_reddit_post_data,
    find_relevant_subreddits
)

from tools.web_scraper_tools import (
    scrape_website_to_markdown,
)

# Tool categories
GOOGLE_TOOLS = [
    search_google,
    search_google_trends,
    search_google_shopping,
    search_google_news,
    smart_search_google_trends
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

# Export all tools for backward compatibility
__all__ = [
    # Individual Tools
    'search_google',
    'search_google_trends',
    'search_google_shopping',
    'search_google_news',
    'smart_search_google_trends',
    'search_youtube',
    'get_youtube_comments',
    'summarize_youtube_transcript',
    'get_reddit_post_data',
    'find_relevant_subreddits',
    'scrape_website_to_markdown',
    
    # Tool Categories
    'GOOGLE_TOOLS',
    'YOUTUBE_TOOLS', 
    'REDDIT_TOOLS',
    'WEB_SCRAPER_TOOLS',
    'ALL_TOOLS'
]
