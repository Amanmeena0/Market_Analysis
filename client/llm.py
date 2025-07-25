import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crewai import LLM
from config import google_api_key


llm = LLM(model="gemini/gemini-2.0-flash", api_key=google_api_key, temperature=0.5)

