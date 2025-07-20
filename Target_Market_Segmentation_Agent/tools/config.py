"""
Configuration and initialization for all tools
"""
import os
import logging
from dotenv import load_dotenv
from crewai import LLM
import praw

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Keys
serper_api_key = os.getenv("SERPER_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")

# Reddit credentials
CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_SECRET") 
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME", "Pretend_Astronomer34")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD", "xUL9htiFDB3r8S")

# Initialize LLM for transcript summarization
try:
    llm = LLM(model="gemini/gemini-1.5-flash", api_key=google_api_key)
except Exception as e:
    logger.warning(f"Could not initialize LLM: {e}")
    llm = None

# Initialize Reddit client
try:
    if CLIENT_ID and CLIENT_SECRET and REDDIT_USERNAME and REDDIT_PASSWORD:
        USER_AGENT = f"MySearchScript/1.0 by u/{REDDIT_USERNAME}"
        reddit = praw.Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            username=REDDIT_USERNAME,
            password=REDDIT_PASSWORD,
            user_agent=USER_AGENT,
        )
    else:
        reddit = None
        logger.warning("Reddit credentials not found")
except Exception as e:
    reddit = None
    logger.warning(f"Could not initialize Reddit client: {e}")
