import uvicorn
from fastapi import FastAPI
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from google_tools import google_mcp
from reddit_tools import reddit_mcp
from scraper_tools import scraper_mcp
from youtube_tools import youtube_mcp

app = FastAPI(title="Market Research MCP Server", version="1.0.0")

# Mount available MCP servers
app.mount("/mcp/google_mcp", google_mcp.sse_app())
app.mount("/mcp/reddit_mcp", reddit_mcp.sse_app())
app.mount("/mcp/scraper_mcp", scraper_mcp.sse_app())
app.mount("/mcp/youtube_mcp", youtube_mcp.sse_app())

available_servers = []

available_servers.append("/mcp/google_mcp")
available_servers.append("/mcp/reddit_mcp")
available_servers.append("/mcp/scraper_mcp")
available_servers.append("/mcp/youtube_mcp")

@app.get("/")
async def root():
    return {
        "message": "Market Research MCP Server",
        "available_servers": available_servers,
        "total_servers": len(available_servers)
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=3000,
    )