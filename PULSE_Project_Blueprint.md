# 🎯 PULSE — Project Blueprint
## Real-Time Sentiment Intelligence Platform
### *"What's moving before it moves"*

---

**Team:** Aayush (AI/Development Lead) + Friend (Data Analysis/QA)  
**Budget:** $100-150/month  
**Tools Available:** Claude Code Pro, ChatGPT Pro, Gemini

---

## 📊 Executive Summary

PULSE aggregates user-generated content from X/Twitter, Reddit, and Polymarket to identify emerging market trends before mainstream news coverage. Unlike prediction tools, PULSE is an **insight platform** — surfacing what crowds are discussing so users can make their own informed decisions.

**Example Use Case:** RAM shortage discussions appeared on Reddit/X weeks before SanDisk stock moved +200%. PULSE would have surfaced this signal.

---

## 💰 Budget Allocation (Monthly)

| Category | Service | Cost | Notes |
|----------|---------|------|-------|
| **Database** | Supabase Pro | $25 | 8GB DB, 100K MAU, daily backups |
| **Hosting** | Railway Hobby | $5 | $5 credits included, usage-based |
| **AI Processing** | Claude API (Sonnet 4.5) | $30-50 | ~$3/1M input, $15/1M output |
| **Cache** | Upstash Redis | $0-10 | Free tier generous, pay as grow |
| **Domain** | Namecheap/Cloudflare | $10-15/yr | Optional for MVP |
| **Buffer** | Emergency/scaling | $10-20 | API overages |
| **Total** | | **$70-110/mo** | Well under budget |

### Free Resources You Already Have
- **Claude Code Pro** — For all development work
- **ChatGPT Pro** — Secondary AI for testing/comparison  
- **Gemini** — Additional AI perspective

---

## 🔌 Data Source Analysis

### 1. Reddit API — **START HERE** ✅

| Aspect | Details |
|--------|---------|
| **Cost** | FREE for non-commercial/research |
| **Rate Limit** | 100 requests/min (OAuth) |
| **Complexity** | Low — PRAW library is excellent |
| **Signal Quality** | HIGH — r/stocks, r/wallstreetbets, r/technology |
| **Why First** | Easiest API, best documentation, highest signal-to-noise |

**Target Subreddits:**
- `r/wallstreetbets` — High volume, needs filtering
- `r/stocks` — Moderate, quality discussions
- `r/investing` — Long-term plays
- `r/technology` — Supply chain signals (RAM, chips)
- `r/hardware` — Technical product discussions
- `r/options` — Unusual activity signals

### 2. Polymarket API — **PHASE 2** ✅

| Aspect | Details |
|--------|---------|
| **Cost** | FREE — All read operations |
| **Rate Limit** | 1,000 calls/hour (non-trading) |
| **Complexity** | Medium — REST + WebSocket |
| **Signal Quality** | VERY HIGH — Crowd probability = quantified sentiment |
| **Documentation** | docs.polymarket.com |

**Key Signals:**
- Rapid probability shifts (>10% in 24h)
- High volume markets (attention indicator)
- Divergence from news narrative

### 3. X/Twitter — **PHASE 3** ⚠️

| Aspect | Details |
|--------|---------|
| **Official API Cost** | $200/mo Basic, $5000/mo Pro |
| **Free Tier** | Write-only, essentially useless |
| **Alternative** | Grok (requires X Premium+ $40/mo) |
| **Workaround** | Twikit library (scraping, use carefully) |
| **Recommendation** | Defer until revenue or use Grok via X Premium |

**Strategy for MVP:** Skip official X API. Use Grok's built-in X search if you have X Premium, or defer Twitter integration to V2.

---

## 🏗️ Architecture Overview

```
┌────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                             │
├──────────────────┬──────────────────┬─────────────────────────┤
│   Reddit API     │  Polymarket API  │    X/Grok (V2)          │
│   (PRAW/Python)  │  (REST/WebSocket)│    (Twikit/Premium)     │
└────────┬─────────┴────────┬─────────┴───────────┬─────────────┘
         │                  │                     │
         ▼                  ▼                     ▼
┌────────────────────────────────────────────────────────────────┐
│                    PROCESSING LAYER                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Ingest   │→ │ Clean &  │→ │ Entity   │→ │ Claude   │       │
│  │ Queue    │  │ Dedup    │  │ Extract  │  │ Synthesis│       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│                                                                │
│  Upstash Redis          Python/FastAPI        Claude Sonnet   │
└────────────────────────────────┬───────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────┐
│                      STORAGE LAYER                             │
│                                                                │
│   Supabase (PostgreSQL)                                        │
│   ├── raw_signals (incoming data)                              │
│   ├── insights (Claude-generated analysis)                     │
│   ├── tracked_assets (sentiment scores)                        │
│   └── signal_timeseries (historical trends)                    │
│                                                                │
└────────────────────────────────┬───────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────┐
│                       API LAYER                                │
│                                                                │
│   FastAPI Backend (Railway)                                    │
│   ├── /api/insights — Get current hot topics                   │
│   ├── /api/signals — Live feed                                 │
│   ├── /api/assets/{symbol} — Asset deep dive                   │
│   └── WebSocket — Real-time updates                            │
│                                                                │
└────────────────────────────────┬───────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────┐
│                     FRONTEND LAYER                             │
│                                                                │
│   React + TypeScript + Tailwind + Framer Motion                │
│   ├── Dashboard (What's Hot)                                   │
│   ├── Live Signal Feed                                         │
│   ├── Asset Watchlist                                          │
│   └── Sentiment Radar                                          │
│                                                                │
│   Hosted: Vercel (free) or Railway                             │
└────────────────────────────────────────────────────────────────┘
```

---

## 👥 Team Role Division

### Aayush (AI/Development Lead)
- **Primary:** All coding, AI integration, architecture decisions
- **Tools:** Claude Code Pro for development, ChatGPT/Gemini for testing
- **Focus Areas:**
  - Backend development (FastAPI)
  - Frontend development (React)
  - AI prompt engineering (Claude synthesis)
  - Database schema design
  - API integrations

### Friend (Data Analysis/QA Lead)
- **Primary:** Data validation, insight quality, user perspective
- **Tools:** Supabase dashboard (SQL), spreadsheets, manual testing
- **Focus Areas:**
  - Writing SQL queries to validate data quality
  - Testing insight accuracy (did the signal predict the move?)
  - Identifying false positives/noise
  - User experience feedback
  - Creating "paper trail" documentation (signal → outcome)
  - Defining credibility scoring rules

### Collaboration Points
| Task | Aayush | Friend |
|------|--------|--------|
| Define credibility rules | Implements logic | Defines rules from data |
| Test signal quality | Builds testing tools | Runs tests, reports issues |
| Design dashboard | Builds UI | Reviews, suggests changes |
| Validate insights | Reviews AI output | Cross-checks with reality |
| Documentation | Technical docs | User guides, signal tracking |

---

## 📅 Phase-by-Phase Roadmap

---

### **PHASE 1: Foundation** (Week 1-2)
**Goal:** Basic infrastructure + Reddit pipeline working

#### Week 1: Setup & Reddit Integration

| Day | Aayush Tasks | Friend Tasks |
|-----|--------------|--------------|
| 1-2 | Set up Supabase project, create DB schema | Research target subreddits, create list |
| 3-4 | Create Reddit API credentials, test PRAW | Document what "quality signal" looks like |
| 5 | Build basic Reddit scraper (hot posts) | Test scraper output, identify issues |
| 6-7 | Set up FastAPI skeleton on Railway | Review API structure, suggest endpoints |

#### Week 2: Processing Pipeline

| Day | Aayush Tasks | Friend Tasks |
|-----|--------------|--------------|
| 1-2 | Build entity extraction (tickers, companies) | Create ticker/company mapping spreadsheet |
| 3-4 | Implement basic sentiment scoring | Validate sentiment accuracy on samples |
| 5 | Connect scraper → DB pipeline | Write SQL to verify data is storing |
| 6-7 | Add basic Claude synthesis call | Review Claude output quality |

#### Phase 1 Checklist
**Aayush:**
- [ ] Supabase project created
- [ ] Database schema deployed (raw_signals, insights, tracked_assets)
- [ ] Reddit API credentials obtained
- [ ] PRAW scraper fetching r/stocks hot posts
- [ ] FastAPI running on Railway
- [ ] Basic Claude API call working
- [ ] Data flowing: Reddit → Processing → Supabase

**Friend:**
- [ ] List of 10 target subreddits with reasoning
- [ ] Credibility scoring v1 document (what makes a quality post?)
- [ ] 20 sample posts manually scored for sentiment
- [ ] SQL queries to check data quality
- [ ] Signal tracking spreadsheet started

#### Phase 1 Budget Check
- Supabase Pro: $25
- Railway: ~$2-5 (low usage)
- Claude API: ~$5-10 (testing)
- **Total: ~$35**

---

### **PHASE 2: Intelligence Layer** (Week 3-4)
**Goal:** Claude-powered insight generation + Polymarket integration

#### Week 3: Claude Synthesis Engine

| Day | Aayush Tasks | Friend Tasks |
|-----|--------------|--------------|
| 1-2 | Design Claude synthesis prompt | Write desired output format |
| 3-4 | Build insight aggregation pipeline | Test insight quality, rate 1-10 |
| 5 | Implement confidence scoring | Define confidence thresholds |
| 6-7 | Add asset mapping (discussion → ticker) | Create asset mapping reference |

#### Week 4: Polymarket Integration

| Day | Aayush Tasks | Friend Tasks |
|-----|--------------|--------------|
| 1-2 | Build Polymarket API client | Research interesting markets to track |
| 3-4 | Implement probability change detection | Define "significant" probability shift |
| 5 | Create cross-source triangulation | Test triangulation logic |
| 6-7 | Build unified insight generation | Validate cross-source insights |

#### Phase 2 Checklist
**Aayush:**
- [ ] Claude synthesis prompt finalized
- [ ] Insight generation pipeline working
- [ ] Confidence scores calculated
- [ ] Polymarket client fetching data
- [ ] Probability momentum detection working
- [ ] Cross-source triangulation implemented
- [ ] Insights table populated automatically

**Friend:**
- [ ] Insight quality rubric created
- [ ] 50 insights manually reviewed and scored
- [ ] False positive patterns documented
- [ ] Asset mapping spreadsheet (100+ entries)
- [ ] Polymarket markets of interest list

#### Phase 2 Budget Check
- Supabase Pro: $25
- Railway: ~$5-10
- Claude API: ~$20-30 (more processing)
- **Total: ~$55-70**

---

### **PHASE 3: Frontend & Real-Time** (Week 5-6)
**Goal:** Beautiful dashboard with live updates

#### Week 5: Core Dashboard

| Day | Aayush Tasks | Friend Tasks |
|-----|--------------|--------------|
| 1-2 | React project setup, Tailwind config | Sketch dashboard wireframe |
| 3-4 | Build "What's Hot" component | Review, suggest improvements |
| 5 | Build Live Signal Feed | Test feed usability |
| 6-7 | Build Asset Watchlist | Add/remove assets, test UX |

#### Week 6: Polish & Real-Time

| Day | Aayush Tasks | Friend Tasks |
|-----|--------------|--------------|
| 1-2 | Implement WebSocket for live updates | Test update latency |
| 3-4 | Add Framer Motion animations | Review animation smoothness |
| 5 | Build Sentiment Radar chart | Verify data accuracy in chart |
| 6-7 | Mobile responsiveness | Test on phone/tablet |

#### Phase 3 Checklist
**Aayush:**
- [ ] React + TypeScript + Tailwind setup
- [ ] "What's Hot" cards rendering
- [ ] Live signal feed working
- [ ] Asset watchlist with add/remove
- [ ] WebSocket real-time updates
- [ ] Sentiment radar chart
- [ ] Dark mode implemented
- [ ] Mobile responsive

**Friend:**
- [ ] Dashboard wireframe approved
- [ ] Usability testing (5 tasks completed)
- [ ] Mobile testing on 2 devices
- [ ] Bug list documented
- [ ] Suggested improvements list

#### Phase 3 Budget Check
- Supabase Pro: $25
- Railway: ~$10-15
- Claude API: ~$30-40
- **Total: ~$70-85**

---

### **PHASE 4: Launch Prep** (Week 7-8)
**Goal:** Production-ready MVP

#### Week 7: Hardening

| Day | Aayush Tasks | Friend Tasks |
|-----|--------------|--------------|
| 1-2 | Add user authentication (Supabase Auth) | Test auth flow |
| 3-4 | Implement rate limiting | Try to break it |
| 5 | Error handling, logging | Review error messages |
| 6-7 | Performance optimization | Test load times |

#### Week 8: Launch

| Day | Aayush Tasks | Friend Tasks |
|-----|--------------|--------------|
| 1-2 | Final bug fixes | Full app walkthrough |
| 3-4 | Deploy to production | Verify production works |
| 5 | Create landing page | Write copy for landing |
| 6-7 | Soft launch to 5-10 users | Gather feedback |

#### Phase 4 Checklist
**Aayush:**
- [ ] Supabase Auth implemented
- [ ] Rate limiting on all endpoints
- [ ] Error boundaries in React
- [ ] API error handling
- [ ] Production deployment
- [ ] Custom domain configured
- [ ] Analytics (Plausible/Umami)

**Friend:**
- [ ] Full QA pass completed
- [ ] Edge case testing
- [ ] Landing page copy written
- [ ] 5 beta users recruited
- [ ] Feedback collection system

#### Phase 4 Budget Check
- Supabase Pro: $25
- Railway: ~$15-20
- Claude API: ~$40-50
- Domain: ~$10
- **Total: ~$95-110**

---

## 🗄️ Database Schema

```sql
-- Core signal storage
CREATE TABLE raw_signals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source VARCHAR(50) NOT NULL,      -- 'reddit', 'polymarket', 'twitter'
    source_id VARCHAR(255),           -- Original post ID
    content TEXT,
    author_id VARCHAR(255),
    author_credibility FLOAT DEFAULT 0.5,
    engagement_metrics JSONB,         -- {upvotes, comments, awards}
    extracted_entities JSONB,         -- {tickers: [], companies: []}
    sentiment_score FLOAT,            -- -1 to 1
    urgency_score FLOAT,              -- 0 to 1
    created_at TIMESTAMPTZ DEFAULT NOW(),
    source_created_at TIMESTAMPTZ,
    processed BOOLEAN DEFAULT FALSE
);

-- Claude-generated insights
CREATE TABLE insights (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    theme VARCHAR(500),
    confidence_score FLOAT,           -- 0 to 1
    sources_agreeing TEXT[],          -- ['reddit', 'polymarket']
    related_assets TEXT[],            -- ['$WDC', '$STX']
    sentiment VARCHAR(20),            -- 'bullish', 'bearish', 'neutral'
    urgency VARCHAR(20),              -- 'immediate', 'developing', 'background'
    evidence JSONB,                   -- Supporting quotes
    signal_ids UUID[],                -- References to raw_signals
    created_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ            -- Insights decay
);

-- Asset tracking
CREATE TABLE tracked_assets (
    symbol VARCHAR(20) PRIMARY KEY,
    asset_type VARCHAR(50),           -- 'stock', 'crypto', 'commodity'
    current_sentiment FLOAT,
    mention_velocity FLOAT,           -- Mentions per hour
    last_insight_id UUID,
    last_updated TIMESTAMPTZ
);

-- Historical time-series
CREATE TABLE signal_timeseries (
    time TIMESTAMPTZ NOT NULL,
    asset_symbol VARCHAR(20),
    mention_count INTEGER,
    avg_sentiment FLOAT,
    source VARCHAR(50)
);

-- For Friend's analysis
CREATE VIEW daily_signal_summary AS
SELECT 
    DATE(source_created_at) as day,
    source,
    COUNT(*) as signal_count,
    AVG(sentiment_score) as avg_sentiment,
    COUNT(DISTINCT extracted_entities->>'tickers') as unique_tickers
FROM raw_signals
GROUP BY DATE(source_created_at), source;
```

---

## 🤖 Claude Synthesis Prompt

```python
SYNTHESIS_PROMPT = """
You are a financial signal analyst. Analyze aggregated social data to identify 
emerging themes and market opportunities. DO NOT make predictions — only 
synthesize what the data objectively shows.

## Input Data
- Reddit signals: {reddit_signals}
- Polymarket data: {polymarket_signals}

## Analysis Requirements
1. Identify emerging themes across sources
2. Note cross-source agreement (higher confidence)
3. Map discussions to tradeable assets
4. Filter noise from real signals
5. Assign urgency levels

## Output Format (JSON)
{{
    "emerging_themes": [
        {{
            "theme": "Brief description",
            "confidence": 0.0-1.0,
            "sources_agreeing": ["reddit", "polymarket"],
            "key_evidence": ["quote1", "quote2"],
            "related_assets": ["$TICKER1", "commodity"],
            "sentiment": "bullish|bearish|neutral",
            "urgency": "immediate|developing|background"
        }}
    ],
    "source_divergences": [
        // Where sources disagree — interesting to note
    ],
    "noise_filtered": [
        // Topics that look like signals but are memes/spam
    ]
}}

## Confidence Scoring
- 0.9+: Multiple sources, high engagement, clear asset connection
- 0.7-0.9: Single source but strong signal, or multi-source weak
- 0.5-0.7: Emerging pattern, needs monitoring
- <0.5: Noise or isolated mention

Be conservative. False negatives are better than false positives.
"""
```

---

## 📁 Project Structure

```
pulse/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app
│   │   ├── config.py               # Environment config
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── insights.py     # GET /insights
│   │   │   │   ├── signals.py      # GET /signals
│   │   │   │   └── websocket.py    # Real-time
│   │   ├── services/
│   │   │   ├── reddit_scraper.py   # PRAW integration
│   │   │   ├── polymarket.py       # Polymarket client
│   │   │   ├── claude_synth.py     # AI synthesis
│   │   │   └── signal_processor.py # Processing pipeline
│   │   └── models/
│   │       └── schemas.py          # Pydantic models
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── dashboard/
│   │   │   │   ├── HotTopicsCard.tsx
│   │   │   │   ├── LiveFeed.tsx
│   │   │   │   ├── AssetWatchlist.tsx
│   │   │   │   └── SentimentRadar.tsx
│   │   │   └── ui/                 # shadcn components
│   │   ├── hooks/
│   │   │   ├── useInsights.ts
│   │   │   └── useWebSocket.ts
│   │   ├── lib/
│   │   │   ├── api.ts
│   │   │   └── supabase.ts
│   │   └── pages/
│   │       ├── Dashboard.tsx
│   │       └── AssetDetail.tsx
│   ├── package.json
│   └── tailwind.config.js
│
├── data/                           # Friend's analysis
│   ├── signal_tracking.xlsx        # Manual tracking
│   ├── credibility_rules.md
│   └── asset_mapping.csv
│
└── docs/
    ├── API.md
    ├── SETUP.md
    └── CHANGELOG.md
```

---

## 🔧 Key Code Templates

### Reddit Scraper (backend/app/services/reddit_scraper.py)

```python
import praw
from datetime import datetime
from typing import List, Dict

class RedditScraper:
    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        
        self.target_subreddits = [
            "wallstreetbets", "stocks", "investing",
            "technology", "hardware", "options"
        ]
    
    async def fetch_hot_posts(self, limit: int = 100) -> List[Dict]:
        signals = []
        
        for sub_name in self.target_subreddits:
            subreddit = self.reddit.subreddit(sub_name)
            
            for post in subreddit.hot(limit=limit):
                if self._passes_filter(post):
                    signals.append({
                        "source": "reddit",
                        "source_id": post.id,
                        "content": f"{post.title}\n\n{post.selftext}",
                        "author_id": str(post.author),
                        "engagement_metrics": {
                            "upvotes": post.score,
                            "comments": post.num_comments,
                            "upvote_ratio": post.upvote_ratio
                        },
                        "source_created_at": datetime.fromtimestamp(post.created_utc),
                        "subreddit": sub_name
                    })
        
        return signals
    
    def _passes_filter(self, post) -> bool:
        """Basic quality filter"""
        return (
            post.score > 50 and
            post.num_comments > 10 and
            not post.stickied and
            len(post.title) > 10
        )
```

### Claude Synthesis (backend/app/services/claude_synth.py)

```python
import anthropic
import json
from typing import Dict, List

class ClaudeSynthesizer:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
    
    async def synthesize(
        self, 
        reddit_signals: List[Dict],
        polymarket_signals: List[Dict]
    ) -> Dict:
        prompt = f"""
        Analyze these signals and identify emerging themes.
        
        Reddit Signals:
        {json.dumps(reddit_signals[:20], indent=2)}  # Limit for token management
        
        Polymarket Data:
        {json.dumps(polymarket_signals[:10], indent=2)}
        
        Output JSON with emerging_themes, source_divergences, noise_filtered.
        """
        
        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse JSON from response
        return json.loads(response.content[0].text)
```

### Frontend Hot Topics (frontend/src/components/dashboard/HotTopicsCard.tsx)

```tsx
import { motion } from 'framer-motion';

interface Insight {
  id: string;
  theme: string;
  confidence: number;
  sources_agreeing: string[];
  related_assets: string[];
  sentiment: 'bullish' | 'bearish' | 'neutral';
  urgency: 'immediate' | 'developing' | 'background';
}

export function HotTopicsCard({ insights }: { insights: Insight[] }) {
  return (
    <div className="bg-gray-900/50 backdrop-blur-xl rounded-2xl p-6 border border-gray-800">
      <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
        <span className="text-2xl">🔥</span> What's Hot Right Now
      </h2>
      
      <div className="space-y-4">
        {insights.map((insight, idx) => (
          <motion.div
            key={insight.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
            className="bg-gray-800/50 rounded-xl p-4 border border-gray-700/50"
          >
            <div className="flex justify-between items-start mb-2">
              <h3 className="text-white font-medium">{insight.theme}</h3>
              <span className={`px-2 py-1 rounded-full text-xs ${
                insight.urgency === 'immediate' ? 'bg-red-500/20 text-red-400' :
                insight.urgency === 'developing' ? 'bg-yellow-500/20 text-yellow-400' :
                'bg-gray-500/20 text-gray-400'
              }`}>
                {insight.urgency}
              </span>
            </div>
            
            <div className="flex items-center gap-4 text-sm text-gray-400">
              <span>Confidence: {Math.round(insight.confidence * 100)}%</span>
              <span>Sources: {insight.sources_agreeing.join(', ')}</span>
            </div>
            
            <div className="flex gap-2 mt-3">
              {insight.related_assets.map(asset => (
                <span 
                  key={asset}
                  className="px-2 py-1 bg-blue-500/20 text-blue-400 rounded text-xs"
                >
                  {asset}
                </span>
              ))}
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
```

---

## 📊 Friend's Analysis Templates

### Signal Tracking Spreadsheet Columns

| Column | Description | Example |
|--------|-------------|---------|
| Date Discovered | When PULSE surfaced it | 2025-01-15 |
| Theme | What the signal was about | RAM shortage |
| Source(s) | Where it came from | Reddit, Polymarket |
| Confidence | PULSE confidence score | 0.87 |
| Related Assets | What to watch | $WDC, $STX, $MU |
| Price at Discovery | Asset price when found | $48.50 |
| Outcome Date | When outcome became clear | 2025-02-01 |
| Price at Outcome | Asset price at outcome | $72.30 |
| Actual Move | Percentage change | +49% |
| Signal Accuracy | Did it predict correctly? | ✅ Yes |
| Notes | Learnings | Early signal, high confidence worked |

### SQL Queries for Analysis

```sql
-- Signal volume by source
SELECT source, DATE(created_at) as day, COUNT(*) 
FROM raw_signals 
GROUP BY source, DATE(created_at)
ORDER BY day DESC;

-- High confidence insights
SELECT theme, confidence_score, sources_agreeing, related_assets
FROM insights
WHERE confidence_score > 0.8
ORDER BY created_at DESC
LIMIT 20;

-- Asset mention velocity
SELECT 
    asset,
    COUNT(*) as mentions,
    AVG(sentiment_score) as avg_sentiment
FROM raw_signals, 
     jsonb_array_elements_text(extracted_entities->'tickers') as asset
WHERE created_at > NOW() - INTERVAL '24 hours'
GROUP BY asset
ORDER BY mentions DESC;
```

---

## ⚠️ Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Reddit API changes | Cache data, build backup scraping option |
| API costs spike | Set hard spending limits, implement rate limiting |
| False signals | Conservative confidence thresholds, human review |
| Legal concerns | Clear "not financial advice" disclaimers |
| X API too expensive | Defer to V2, use Grok if Premium available |

---

## 🎯 Success Metrics (V1)

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Signal accuracy | >60% | Manual tracking by Friend |
| Signal lead time | >24 hours | Time between signal and price move |
| User engagement | 5+ daily users | Analytics |
| System uptime | >99% | Railway monitoring |
| API cost efficiency | <$100/mo | Supabase + Railway dashboards |

---

## 💡 Suggestions

1. **Start with Reddit only** — Get one pipeline perfect before adding complexity
2. **Build the "paper trail" early** — Friend tracking signal → outcome is your proof
3. **Conservative confidence scoring** — False negatives are better than false positives
4. **Time decay everything** — A signal from 2 hours ago is worth more than one from yesterday
5. **Ship fast, iterate faster** — Get something working in 2 weeks, improve from there
6. **Use Claude Code Pro heavily** — Let it write boilerplate, you focus on logic
7. **Document learnings** — What worked, what didn't — this is IP

---

## 🚀 Next Steps

**This Week:**
1. Aayush: Create Supabase project + Reddit API credentials
2. Friend: Research and document target subreddits with reasoning
3. Both: Agree on MVP scope (features in, features out)

**End of Week 1:**
- Reddit data flowing into database
- Basic API endpoint returning raw signals
- Friend validating data quality

---

*Document Version: 1.0*  
*Last Updated: January 25, 2026*  
*Team: Aayush + Friend*
