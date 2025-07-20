"""
Reddit related tools for community sentiment and discussion analysis
"""
import json
from crewai.tools import tool
from .config import reddit, logger


@tool("RedditSearchTool")
def get_reddit_post_data(query: str, subreddit_name: str = "all", max_posts: int = 5) -> str:
    """
    Search Reddit for posts and comments related to a specific topic.
    
    Args:
        query (str): The search term to look for
        subreddit_name (str): The subreddit to search in (default: "all")
        max_posts (int): Maximum number of posts to return (max: 10)
        
    Returns:
        str: Comprehensive Reddit sentiment and discussion analysis
    """
    try:
        if not reddit:
            return "Error: Reddit client not initialized. Check credentials"

        if max_posts > 10:
            max_posts = 10

        subreddit = reddit.subreddit(subreddit_name)
        search_results = list(subreddit.search(query, sort='relevance', limit=max_posts))

        if not search_results:
            all_reddits = reddit.subreddit("all")
            search_results = list(all_reddits.search(query, sort='relevance', limit=max_posts))

        if not search_results:
            return f"No Reddit discussions found for '{query}'"

        analysis = f"Reddit Discussion Analysis for '{query}':\n\n"
        analysis += f"Analysis Summary:\n"
        analysis += f"- Posts analyzed: {len(search_results)}\n"
        analysis += f"- Subreddit: r/{subreddit_name}\n\n"
        
        total_comments = 0
        positive_keywords = ['good', 'great', 'love', 'awesome', 'excellent', 'amazing', 'best']
        negative_keywords = ['bad', 'terrible', 'hate', 'awful', 'worst', 'disappointing']
        
        analysis += "Key Discussions:\n"
        
        for i, submission in enumerate(search_results, 1):
            comment_count = 0
            sentiment_indicators = {'positive': 0, 'negative': 0}
            
            # Analyze post title and text
            post_text = f"{submission.title} {submission.selftext}".lower()
            for word in positive_keywords:
                sentiment_indicators['positive'] += post_text.count(word)
            for word in negative_keywords:
                sentiment_indicators['negative'] += post_text.count(word)
            
            # Analyze sentiment from post content and comment count
            comment_count = submission.num_comments
            
            # Basic sentiment analysis on post title and text
            for word in positive_keywords:
                sentiment_indicators['positive'] += post_text.count(word)
            for word in negative_keywords:
                sentiment_indicators['negative'] += post_text.count(word)
            
            total_comments += comment_count
            
            # Determine sentiment
            if sentiment_indicators['positive'] > sentiment_indicators['negative']:
                sentiment = "Positive"
            elif sentiment_indicators['negative'] > sentiment_indicators['positive']:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"
            
            analysis += f"{i}. r/{submission.subreddit.display_name}: {submission.title}\n"
            analysis += f"   Comments: {comment_count} | Sentiment: {sentiment}\n"
            analysis += f"   URL: https://reddit.com{submission.permalink}\n\n"
        
        analysis += f"Overall Insights:\n"
        analysis += f"- Total comments analyzed: {total_comments}\n"
        analysis += f"- Most active discussions found in: {', '.join(set([s.subreddit.display_name for s in search_results]))}\n"
        
        return analysis
    except Exception as e:
        logger.error(f"Error in get_reddit_post_data: {e}")
        return f"Error searching Reddit: {str(e)}"


@tool("RedditSubredditFinder")
def find_relevant_subreddits(keywords: str, limit: int = 10) -> str:
    """
    Find subreddits relevant to specific keywords for targeted market research.
    
    Args:
        keywords (str): Space-separated keywords to search for
        limit (int): Maximum number of subreddits to return (default: 10)
        
    Returns:
        str: Analysis of relevant subreddits with community insights
    """
    try:
        if not reddit:
            return "Error: Reddit client not initialized. Check credentials"

        keywords_list = keywords.split()
        query = " ".join(keywords_list)
        
        subreddits_list = list(reddit.subreddits.search(query, limit=limit))
        subreddit_data = []
        
        for sub in subreddits_list:
            try:
                subreddit_data.append({
                    'name': sub.display_name,
                    'description': sub.public_description or 'No description available',
                    'subscribers': getattr(sub, 'subscribers', 'Unknown')
                })
            except Exception:
                continue  # Skip subreddits that can't be accessed
        
        if not subreddit_data:
            return f"No subreddits found for keywords: '{query}'"
        
        analysis = f"Relevant Subreddits Analysis for '{query}':\n\n"
        analysis += f"Found {len(subreddit_data)} relevant communities:\n\n"
        
        for i, sub in enumerate(subreddit_data, 1):
            analysis += f"{i}. r/{sub['name']}\n"
            analysis += f"   Subscribers: {sub['subscribers']}\n"
            analysis += f"   Description: {sub['description'][:100]}...\n\n"
        
        analysis += "Community Insights:\n"
        analysis += f"- Total communities found: {len(subreddit_data)}\n"
        analysis += f"- Search keywords: {keywords}\n"
        analysis += f"- These communities can provide valuable market insights and customer feedback\n"
        
        return analysis
    except Exception as e:
        logger.error(f"Error in find_relevant_subreddits: {e}")
        return f"Error finding subreddits: {str(e)}"
