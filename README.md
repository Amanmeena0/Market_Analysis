# Market Analysis Platform

A comprehensive AI-powered market analysis platform that provides in-depth insights across multiple business domains. The platform combines web scraping, data analysis, and AI agents to generate detailed market research reports.

## Features

- **Multi-Agent Analysis System**: Specialized AI agents for different types of market analysis
- **Real-time Web Scraping**: Integration with Google, Reddit, YouTube, and general web scraping tools
- **Interactive Web Interface**: Modern Next.js frontend with PDF report viewing
- **Comprehensive Reports**: Generate detailed PDF reports for analysis results
- **WebSocket Integration**: Real-time communication between frontend and backend

## Analysis Types

The platform supports five main types of market analysis:

1. **Barrier Assessment** - Analyze market entry barriers and challenges
2. **Competitive Analysis** - Research competitors and market positioning
3. **Market Gap Identification** - Identify opportunities and unmet needs
4. **Sales Forecast** - Predict market trends and sales projections
5. **Target Market Segmentation** - Define and analyze target customer segments
6. **Industry Analysis** - Analyze the overall structure, trends, and dynamics of a specific industry.

## Tech Stack

### Backend
- **Python 3.12+** - Core backend language
- **FastAPI** - Web framework and API server
- **LangGraph** - AI agent orchestration
- **MongoDB** - Database for storing analysis data
- **Model Context Protocol (MCP)** - Tool integration framework
- **uvicorn** - ASGI server

### Frontend
- **Next.js 15** - React framework
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first styling
- **ShadCN UI** - Component library
- **React PDF Viewer** - PDF display functionality

## Project Structure

```
Market_Analysis/
├── client/                 # Next.js frontend application
│   ├── src/
│   │   ├── app/           # App router pages
│   │   ├── components/    # React components
│   │   └── lib/          # Utilities and types
│   └── public/           # Static assets
├── server/                # Python backend application
│   ├── agents/           # AI agents for different analysis types
│   ├── config/           # Configuration and settings
│   ├── database/         # Database schemas and connection
│   ├── mcp_servers/      # MCP tool servers
│   ├── prompts/          # AI prompts for different analyses
│   └── reports/          # Generated analysis reports
└── README.md
```

## Usage

1. **Select Analysis Type**: Choose from the five available analysis types
2. **Enter Query**: Provide your market analysis query or business question
3. **Start Analysis**: The AI agents will begin researching using web scraping tools
4. **Real-time Updates**: Monitor progress through WebSocket updates
5. **Download Report**: Once complete, download the generated PDF report

## MCP Tool Servers

The platform includes several MCP (Model Context Protocol) servers for different data sources:

- **Google Tools** - Search and web data collection
- **Reddit Tools** - Social media insights and trends
- **YouTube Tools** - Video content analysis
- **Scraper Tools** - General web scraping capabilities

