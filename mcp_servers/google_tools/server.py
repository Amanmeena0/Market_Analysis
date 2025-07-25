import sys
import os

from mcp.server.fastmcp import FastMCP
from .tools import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

mcp = FastMCP("Google Tools")

mcp.add_tool(google_search)
mcp.add_tool(search_google_shopping)
mcp.add_tool(search_google_news)
mcp.add_tool(google_trends_summary)
