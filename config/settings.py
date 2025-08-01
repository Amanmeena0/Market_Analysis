from dataclasses import dataclass
import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

google_api_key: Optional[str] = os.getenv("GOOGLE_API_KEY")
serp_api_key: Optional[str] = os.getenv("SERP_API_KEY")
serp_dev_api_key: Optional[str] = os.getenv("SERP_DEV_API_KEY")
reddit_client_id: Optional[str] = os.getenv("REDDIT_CLIENT_ID") 
reddit_secret: Optional[str] = os.getenv("REDDIT_SECRET")
reddit_username: Optional[str] = os.getenv("REDDIT_USERNAME") 
reddit_password: Optional[str] = os.getenv("REDDIT_PASSWORD") 


if not google_api_key:
    raise ValueError("Warning: Google API Key is not set. Some features may not work.")

if not reddit_client_id or not reddit_secret:
    raise ValueError("Warning: Reddit Client ID or Secret is not set. Some features may not work.")

if not serp_dev_api_key:
    raise ValueError("Warning: SERP Dev API Key is not set. Some features may not work.")

