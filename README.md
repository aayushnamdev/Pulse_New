# 🎯 PULSE - Real-Time Sentiment Intelligence Platform

> **"What's moving before it moves"**

PULSE is an AI-powered sentiment intelligence platform that aggregates and analyzes user-generated content from Reddit (with planned Polymarket and Twitter integration) to identify emerging market trends before they hit mainstream news.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-brightgreen)
![Railway](https://img.shields.io/badge/Deployed-Railway-purple)
![Claude AI](https://img.shields.io/badge/AI-Claude%204.5%20Sonnet-orange)

## 🚀 Overview

PULSE monitors multiple data sources to surface signals that matter:

- **Reddit Analysis**: Scrapes r/wallstreetbets, r/stocks, r/investing, r/technology, and other high-signal subreddits
- **AI Synthesis**: Uses Claude Sonnet 4.5 to generate narrative wraps and identify emerging themes
- **Quality Filtering**: Advanced filtering to separate signal from noise based on upvotes, engagement, and relevance
- **Automated Pipeline**: Railway cron job running every 6 hours to capture fresh market sentiment

### 📊 Key Features

✅ **Multi-Subreddit Monitoring** - Tracks 5+ high-value subreddits simultaneously
✅ **Intelligence Layer** - Claude AI processes raw signals into actionable insights
✅ **Quality Signal Detection** - Filters posts based on upvotes, engagement, and market relevance
✅ **Narrative Wrapping** - Generates concise summaries of emerging market discussions
✅ **Automated Data Pipeline** - Continuous signal collection and processing
✅ **Supabase Integration** - Scalable PostgreSQL backend for signal storage and analysis

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      DATA SOURCES                           │
│          Reddit API (PRAW) - Multi-Subreddit Scraping       │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   PROCESSING PIPELINE                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Scraper  │→ │ Quality  │→ │ Claude   │→ │ Storage  │    │
│  │ Service  │  │ Filter   │  │ AI Layer │  │ Service  │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   SUPABASE DATABASE                         │
│        PostgreSQL + Real-time Subscriptions                 │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ Tech Stack

**Backend**
- Python 3.12
- FastAPI (API framework)
- PRAW (Reddit API wrapper)
- Anthropic Claude API (AI synthesis)
- Supabase (PostgreSQL database)

**Deployment**
- Railway (Cron job hosting)
- Automated deployment via GitHub integration

**AI & Processing**
- Claude Sonnet 4.5 for narrative generation
- Advanced relevance filtering
- Multi-source signal aggregation

## 📋 Current Capabilities

### Reddit Signal Collection
- Monitors multiple subreddits: wallstreetbets, stocks, investing, technology, hardware
- Configurable fetch limits and quality thresholds
- Engagement metrics tracking (upvotes, comments, ratios)
- Time-based scraping (every 6 hours)

### Intelligence Layer
- Claude-powered narrative generation
- Contextual summarization of market discussions
- Asset and entity extraction
- Quality signal identification

### Data Storage
- Raw signals table with full post metadata
- Processed insights storage
- Source URL tracking for verification
- Timestamped data for trend analysis

## 🚦 Getting Started

### Prerequisites
- Python 3.12+
- Supabase account
- Claude API key
- Reddit API credentials (optional for local testing)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/aayushnamdev/Pulse_New.git
cd Pulse_New
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cd backend
cp .env.example .env
# Edit .env with your credentials
```

4. **Set up database**
```bash
# Run schema.sql in your Supabase SQL Editor
# Run intelligence_layer_schema.sql for AI features
```

5. **Test the scraper**
```bash
cd backend
python scraper_service.py
```

For detailed setup instructions, see [backend/README.md](backend/README.md)

## 📊 Database Schema

### Core Tables
- **raw_signals** - Scraped posts with metadata and engagement metrics
- **insights** - Claude-generated analysis and narrative wraps
- **tracked_assets** - Entity extraction and asset mapping
- **signal_timeseries** - Historical trend data

### Key Features
- Multi-subreddit support
- Quality signal flagging
- Source URL tracking
- AI-generated content storage

## 🔍 How It Works

1. **Scraping Phase**: Railway cron job runs `main.py` every 6 hours
2. **Collection**: Fetches top posts from configured subreddits via Reddit API
3. **Filtering**: Applies quality thresholds (min upvotes, upvote ratio, relevance)
4. **AI Processing**: Claude analyzes relevant signals and generates narratives
5. **Storage**: Saves raw signals and insights to Supabase
6. **Analysis**: Data available for querying and trend analysis

## 📈 Example Output

```json
{
  "title": "Discussion about RAM shortage affecting tech stocks",
  "subreddit": "hardware",
  "upvotes": 542,
  "quality_signal": true,
  "narrative_wrap": "Community discussing supply chain constraints in memory chip manufacturing...",
  "source_url": "https://reddit.com/r/hardware/...",
  "scraped_at": "2025-01-27T12:00:00Z"
}
```

## 🎯 Roadmap

### Phase 1 (✅ Completed)
- [x] Reddit multi-subreddit scraping
- [x] Supabase integration
- [x] Quality filtering system
- [x] Railway deployment
- [x] Claude AI integration
- [x] Narrative wrap generation

### Phase 2 (🚧 In Progress)
- [ ] Polymarket integration
- [ ] Cross-source signal triangulation
- [ ] Enhanced asset mapping
- [ ] Historical trend analysis

### Phase 3 (📋 Planned)
- [ ] Twitter/X integration
- [ ] Real-time WebSocket updates
- [ ] Frontend dashboard (React + TypeScript)
- [ ] User authentication
- [ ] API endpoints for public access

## 📁 Project Structure

```
Pulse_New/
├── backend/
│   ├── main.py                      # Railway cron entry point
│   ├── scraper_service.py           # Reddit scraper
│   ├── database_service.py          # Supabase integration
│   ├── signal_processor.py          # AI processing layer
│   ├── relevance_filter.py          # Quality filtering
│   ├── asset_mapping.json           # Entity/ticker mapping
│   ├── schema.sql                   # Database schema
│   ├── intelligence_layer_schema.sql # AI features schema
│   └── requirements.txt             # Python dependencies
├── PULSE_Project_Blueprint.md       # Full project documentation
├── requirements.txt                 # Root dependencies
└── README.md                        # This file
```

## 🔒 Environment Variables

```bash
# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Reddit API (optional for enhanced scraping)
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent

# Claude AI
ANTHROPIC_API_KEY=your_claude_api_key

# Configuration
REDDIT_SUBREDDIT=wallstreetbets,stocks,investing,technology,hardware
MIN_UPVOTES=50
MIN_UPVOTE_RATIO=0.70
REDDIT_FETCH_LIMIT=100
ENVIRONMENT=production
```

## 📊 Performance Metrics

- **Signal Processing**: ~100-200 posts per run
- **Quality Signals**: ~10-30% pass quality filters
- **AI Processing**: ~5-10 seconds per batch
- **Uptime**: 99%+ (Railway monitoring)
- **Cost**: <$100/month (Supabase + Railway + Claude API)

## 🤝 Contributing

This is currently a private research project. For questions or collaboration inquiries, please reach out.

## 📝 Documentation

- [Backend Setup Guide](backend/README.md)
- [Multi-Subreddit Configuration](backend/MULTI_SUBREDDIT_GUIDE.md)
- [Railway Deployment](backend/RAILWAY_DEPLOYMENT.md)
- [Project Blueprint](PULSE_Project_Blueprint.md)

## ⚠️ Disclaimer

PULSE is an informational tool for sentiment analysis and research purposes only. It does not provide financial advice. All signals should be independently verified before making investment decisions.

## 📞 Contact

**Aayush Namdev**
- GitHub: [@aayushnamdev](https://github.com/aayushnamdev)
- LinkedIn: [Connect on LinkedIn](https://www.linkedin.com/in/aayushnamdev)

---

**Built with Claude Code Pro** | **Powered by Claude Sonnet 4.5** | **Data from Reddit API & Supabase**

*Last Updated: January 2025*
