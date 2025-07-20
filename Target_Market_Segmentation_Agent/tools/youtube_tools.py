"""
YouTube related tools for content analysis and research
"""
import json
from crewai.tools import tool
import googleapiclient.discovery
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound # type: ignore
from .config import google_api_key, llm, logger


@tool("YouTubeSearchTool")
def search_youtube(query: str) -> str:
    """
    Search YouTube for videos related to a specific query.
    
    Args:
        query (str): The search term to look for on YouTube
        
    Returns:
        str: Analysis of relevant YouTube content with video insights
    """
    try:
        if not google_api_key:
            return "Error: GOOGLE_API_KEY not found in environment variables"
            
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=google_api_key)
        
        request = youtube.search().list(
            part="snippet",
            q=query,  
            type="video",  
            videoDuration='medium', 
            maxResults=5,  
        )
        
        response = request.execute()
        
        analysis = f"YouTube Content Analysis for '{query}':\n\n"
        analysis += f"Found {len(response['items'])} relevant videos:\n\n"
        
        for i, item in enumerate(response['items'], 1):
            video_id = item['id'].get('videoId', '')
            snippet = item.get('snippet', {})
            title = snippet.get('title', 'No title')
            channel = snippet.get('channelTitle', 'Unknown channel')
            description = snippet.get('description', '')[:200] + "..." if snippet.get('description') else 'No description'
            
            analysis += f"{i}. {title}\n"
            analysis += f"   Channel: {channel}\n"
            analysis += f"   Video ID: {video_id}\n"
            analysis += f"   Description: {description}\n\n"
        
        return analysis
    except Exception as e:
        logger.error(f"Error in search_youtube: {e}")
        return f"Error searching YouTube: {str(e)}"


@tool("YouTubeCommentsTool")
def get_youtube_comments(video_id: str) -> str:
    """
    Fetch comments from a specific YouTube video for sentiment analysis.
    
    Args:
        video_id (str): The YouTube video ID to fetch comments from
        
    Returns:
        str: Sentiment analysis of YouTube comments
    """
    try:
        if not google_api_key:
            return "Error: GOOGLE_API_KEY not found in environment variables"
            
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=google_api_key)
        
        request = youtube.commentThreads().list(
            part="snippet,replies",
            videoId=video_id,
            textFormat="plainText",
            maxResults=30
        )
        
        response = request.execute()
        comments = []

        for item in response.get('items', []):
            comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
            if comment_text.strip():
                comments.append(comment_text)
        
        if not comments:
            return f"No comments found for video ID: {video_id}"
        
        # Basic sentiment analysis
        analysis = f"YouTube Comments Analysis for Video ID: {video_id}\n\n"
        analysis += f"Total Comments Analyzed: {len(comments)}\n\n"
        
        positive_keywords = ['good', 'great', 'love', 'awesome', 'excellent', 'amazing', 'best', 'like']
        negative_keywords = ['bad', 'terrible', 'hate', 'awful', 'worst', 'disappointing', 'dislike']
        
        positive_count = 0
        negative_count = 0
        
        for comment in comments:
            comment_lower = comment.lower()
            for word in positive_keywords:
                positive_count += comment_lower.count(word)
            for word in negative_keywords:
                negative_count += comment_lower.count(word)
        
        analysis += f"Sentiment Indicators:\n"
        analysis += f"- Positive mentions: {positive_count}\n"
        analysis += f"- Negative mentions: {negative_count}\n"
        
        if positive_count > negative_count:
            sentiment = "Positive"
        elif negative_count > positive_count:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        
        analysis += f"- Overall sentiment: {sentiment}\n\n"
        
        analysis += "Sample Comments:\n"
        for i, comment in enumerate(comments[:5], 1):
            analysis += f"{i}. {comment[:100]}...\n"
        
        return analysis
    except Exception as e:
        logger.error(f"Error in get_youtube_comments: {e}")
        return f"Error fetching YouTube comments: {str(e)}"


@tool("YouTubeTranscriptTool")
def summarize_youtube_transcript(video_id: str) -> str:
    """
    Fetch and summarize a YouTube video's transcript for content analysis.
    
    Args:
        video_id (str): The YouTube video ID to get transcript from
        
    Returns:
        str: Summarized transcript content
    """
    try:
        if not llm:
            return "Error: LLM not initialized. Check GOOGLE_API_KEY"
            
        transcript_data = None
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            try:
                transcript_data = transcript_list.find_transcript(['en']).fetch()
            except NoTranscriptFound:
                for tx in transcript_list:
                    transcript_data = tx.translate('en').fetch()
                    break
                
                if not transcript_data:
                     return f"Error: No transcripts found for video ID: {video_id}"

        except TranscriptsDisabled:
            return f"Error: Transcripts are disabled for video ID: {video_id}"
        except Exception as e:
            return f"An unexpected error occurred: {e}"

        transcript_text = " ".join([item.text for item in transcript_data])

        prompt = f"Please provide a concise but comprehensive summary of the following video transcript:\n\n---\n\n{transcript_text}"
        
        response = llm.call(prompt)
        return str(response)
    except Exception as e:
        logger.error(f"Error in summarize_youtube_transcript: {e}")
        return f"Error summarizing transcript: {str(e)}"
