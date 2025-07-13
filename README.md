# YFinance Analysis Project

A comprehensive financial analysis tool using Yahoo Finance data, CrewAI agents, and various APIs for market research and sentiment analysis.

## Features

- **Company Profile Analysis**: Fetch detailed company information using Yahoo Finance
- **Latest News Integration**: Get real-time news using Serper API
- **Sentiment Analysis**: Analyze market sentiment from news and data
- **Risk Assessment**: Evaluate investment risks
- **Competitor Analysis**: Compare companies with their competitors
- **ESG Data**: Environmental, Social, and Governance performance metrics
- **Macroeconomic Indicators**: Regional economic data analysis

## Project Structure

```
├── client/                 # Frontend application
├── server/                 # Backend server with agents
│   ├── agents.py          # CrewAI agents definition
│   ├── app.py             # Main application file
│   ├── crew.py            # Crew configuration
│   ├── task.py            # Task definitions
│   ├── tools.py           # Custom tools for data fetching
│   ├── requirements.txt   # Python dependencies
│   └── serper.ipynb      # Jupyter notebook for testing
├── Notes/                 # Project documentation and diagrams
└── .env.example          # Environment variables template
```

## Setup

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Amanmeena0/Market_Analysis.git
cd Market_Analysis
```

2. Install dependencies:
```bash
cd server
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```

4. Edit `.env` file and add your API keys:
```
SERPER_API_KEY="your_serper_api_key_here"
GOOGLE_API_KEY="your_google_api_key_here"
```

### API Keys Required

- **Serper API**: For news and search functionality
  - Get your key from: https://serper.dev/
- **Google API**: For additional data services
  - Get your key from: https://console.developers.google.com/

## Usage

1. Start the server:
```bash
cd server
python app.py
```

2. The application will start and you can begin using the various analysis tools.

## Tools Available

- `CompanyProfileTool`: Get company basic information
- `LatestNewsTool`: Fetch latest news articles
- `SentimentAnalysisTool`: Analyze text sentiment
- `RiskAssessmentTool`: Assess company risks
- `CompetitorAnalysisTool`: Compare with competitors
- `ESGFetcherTool`: Get ESG scores
- `MacroeconomicDataTool`: Regional economic indicators

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Yahoo Finance for financial data
- CrewAI for agent framework
- Serper for news API services
