# 🚀 Multi-Subreddit Scraping Guide

## ✨ What's New

PULSE now supports scraping **multiple subreddits simultaneously**! Instead of being limited to one subreddit, you can now monitor 3, 5, 10, or more subreddits in a single run.

---

## 📝 How to Configure

### Environment Variable Format

Set multiple subreddits using **comma-separated values**:

```bash
# Single subreddit (old way - still works)
REDDIT_SUBREDDIT=wallstreetbets

# Multiple subreddits (new way!)
REDDIT_SUBREDDIT=wallstreetbets,stocks,investing,options
```

### Examples

**3 Finance Subreddits:**
```bash
REDDIT_SUBREDDIT=wallstreetbets,stocks,investing
```

**10 Diverse Subreddits:**
```bash
REDDIT_SUBREDDIT=wallstreetbets,stocks,investing,options,technology,hardware,cryptocurrency,stockmarket,finance,economy
```

**Supply Chain Focus:**
```bash
REDDIT_SUBREDDIT=supplychain,manufacturing,logistics,technology,hardware
```

---

## ⚙️ How It Works

1. **Sequential Scraping**: Each subreddit is scraped one after another
2. **Rate Limiting**: 1-second delay between subreddits (to be nice to Reddit)
3. **Combined Results**: All posts are merged and saved to the database
4. **Subreddit Tracking**: Each post stores which subreddit it came from

### Execution Flow

```
Start
  ↓
Scrape r/wallstreetbets (100 posts)
  ↓ (1 second delay)
Scrape r/stocks (100 posts)
  ↓ (1 second delay)
Scrape r/investing (100 posts)
  ↓
Combine all posts (300 total)
  ↓
Filter by quality (upvote_ratio, upvotes)
  ↓
Save to Supabase
  ↓
Done
```

---

## 📊 Limitations & Best Practices

### 1. **Reddit Rate Limits**
- **No API Key Used**: We use Reddit's `.json` endpoint (public access)
- **Rate Limit**: ~60 requests per minute
- **Best Practice**: Keep under 20 subreddits to avoid hitting limits
- **If You Hit Limits**: You'll see HTTP 429 errors - reduce subreddit count

### 2. **Railway Timeout**
- **Default Timeout**: 10 minutes per cron job
- **Scraping Time**: ~2-3 seconds per subreddit
- **Max Subreddits**: Theoretically 200+, but recommend <30
- **If You Timeout**: Reduce `REDDIT_FETCH_LIMIT` or number of subreddits

### 3. **Database Storage**
- **Supabase Free Tier**: 500MB database
- **Post Size**: ~2KB per post
- **Capacity**: ~250,000 posts before full
- **Best Practice**: Clean old data periodically (older than 7 days)

### 4. **Processing Time**
| Subreddits | Fetch Limit | Total Posts | Time (approx) |
|------------|-------------|-------------|---------------|
| 1          | 100         | 100         | 3 seconds     |
| 3          | 100         | 300         | 10 seconds    |
| 5          | 100         | 500         | 20 seconds    |
| 10         | 100         | 1000        | 40 seconds    |
| 20         | 100         | 2000        | 90 seconds    |

### 5. **API Costs (Supabase)**
- **Free Tier**: Plenty for personal use
- **Writes**: Each scrape run writes to database
- **Consideration**: More subreddits = more database writes

---

## 🎯 Recommended Configurations

### **Conservative (Safe for 24/7)**
```bash
REDDIT_SUBREDDIT=wallstreetbets,stocks,investing
REDDIT_FETCH_LIMIT=50
```
- 3 subreddits × 50 posts = 150 posts per run
- Runs every 6 hours = 900 posts/day
- Low risk of rate limits

### **Balanced (Recommended)**
```bash
REDDIT_SUBREDDIT=wallstreetbets,stocks,investing,options,technology
REDDIT_FETCH_LIMIT=100
```
- 5 subreddits × 100 posts = 500 posts per run
- Runs every 6 hours = 2,000 posts/day
- Good signal diversity

### **Aggressive (Max Coverage)**
```bash
REDDIT_SUBREDDIT=wallstreetbets,stocks,investing,options,technology,hardware,crypto,stockmarket,finance,economy
REDDIT_FETCH_LIMIT=100
```
- 10 subreddits × 100 posts = 1,000 posts per run
- Runs every 6 hours = 4,000 posts/day
- Higher chance of quality signals

### **Quality Over Quantity**
```bash
REDDIT_SUBREDDIT=stocks,investing,SecurityAnalysis
REDDIT_FETCH_LIMIT=100
MIN_UPVOTE_RATIO=0.80
MIN_UPVOTES=100
```
- Focus on high-quality subreddits
- Stricter filters = fewer but better signals

---

## 🧪 Testing Multi-Subreddit Locally

Test with 2-3 subreddits first:

```bash
cd backend
source venv/bin/activate

# Edit .env
REDDIT_SUBREDDIT=wallstreetbets,stocks

# Test
python test_full_pipeline.py
```

You should see:
```
🔍 Fetching hot posts from r/wallstreetbets...
✅ Fetched 50 posts from r/wallstreetbets
✅ 43 posts passed quality filters from r/wallstreetbets

🔍 Fetching hot posts from r/stocks...
✅ Fetched 50 posts from r/stocks
✅ 38 posts passed quality filters from r/stocks

📊 Total: 81 posts from 2 subreddit(s)
```

---

## 📈 Monitoring & Analytics

### Check Subreddit Distribution in Supabase

```sql
-- How many posts per subreddit?
SELECT
    subreddit,
    COUNT(*) as post_count,
    COUNT(*) FILTER (WHERE is_quality_signal = TRUE) as quality_signals
FROM raw_signals
WHERE scraped_at > NOW() - INTERVAL '24 hours'
GROUP BY subreddit
ORDER BY post_count DESC;
```

### Find Best Performing Subreddit

```sql
-- Which subreddit has the highest quality signal rate?
SELECT
    subreddit,
    COUNT(*) as total_posts,
    COUNT(*) FILTER (WHERE is_quality_signal = TRUE) as quality_signals,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE is_quality_signal = TRUE) / COUNT(*),
        2
    ) as quality_percentage
FROM raw_signals
GROUP BY subreddit
HAVING COUNT(*) > 50  -- Only subreddits with enough data
ORDER BY quality_percentage DESC;
```

---

## ⚠️ Troubleshooting

### "HTTP 429 Too Many Requests"
**Problem**: Hit Reddit's rate limit
**Solution**:
- Reduce number of subreddits
- Increase `time.sleep()` delay in code (currently 1 second)
- Run less frequently (every 12 hours instead of 6)

### "Railway timeout after 10 minutes"
**Problem**: Too many subreddits to scrape in time
**Solution**:
- Reduce `REDDIT_FETCH_LIMIT` from 100 to 50
- Reduce number of subreddits
- Increase Railway timeout (paid plan)

### "Supabase database full"
**Problem**: Too much historical data
**Solution**:
```sql
-- Delete posts older than 7 days
DELETE FROM raw_signals
WHERE created_at < NOW() - INTERVAL '7 days';
```

---

## 🎯 Best Subreddits for PULSE

### **Finance & Trading** (Core)
- `wallstreetbets` - High volume, meme stocks
- `stocks` - Quality discussions
- `investing` - Long-term plays
- `options` - Unusual options activity
- `StockMarket` - General market sentiment
- `SecurityAnalysis` - Deep DD

### **Supply Chain Signals** (Your Edge!)
- `supplychain` - Direct supply chain news
- `manufacturing` - Production issues
- `logistics` - Shipping/transport delays
- `hardware` - Component shortages (RAM, GPUs)
- `technology` - Tech supply chain

### **Crypto** (Optional)
- `cryptocurrency` - General crypto sentiment
- `Bitcoin` - BTC specific
- `ethereum` - ETH specific

### **Economy** (Macro)
- `economy` - Economic indicators
- `Economics` - Academic perspective
- `finance` - Financial news

---

## 📊 Example Railway Configuration

For maximum signal coverage:

```bash
# Railway Variables Tab
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key

# Multi-subreddit configuration
REDDIT_SUBREDDIT=wallstreetbets,stocks,investing,options,technology,hardware,supplychain
REDDIT_FETCH_LIMIT=100

# Quality filters
MIN_UPVOTE_RATIO=0.70
MIN_UPVOTES=50

# Production mode
ENVIRONMENT=production
```

**Result**: 7 subreddits × 100 posts = 700 posts per run, every 6 hours = 2,800 posts/day

---

## 🚀 Next Steps

1. **Test locally** with 2-3 subreddits
2. **Update Railway** environment variable
3. **Monitor logs** for errors
4. **Check Supabase** for data distribution
5. **Adjust** based on results

Happy scraping! 📈
