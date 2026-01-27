# Railway Deployment Guide - PULSE Intelligence Layer

## Overview
The PULSE cron job now runs two steps automatically every 6 hours:
1. **Scraper**: Fetches new Reddit signals
2. **Intelligence Layer**: Processes signals with AI analysis

## Required Environment Variables in Railway

Make sure these are set in your Railway project settings:

### Existing Variables (Already Set)
```bash
SUPABASE_URL=your-project.supabase.co
SUPABASE_KEY=your-anon-key
REDDIT_SUBREDDIT=wallstreetbets,stocks,investing,technology,hardware,energy,semiconductors,economics
REDDIT_FETCH_LIMIT=100
MIN_UPVOTE_RATIO=0.70
MIN_UPVOTES=15
ENVIRONMENT=production
```

### NEW Variables (Add These in Railway Dashboard)
```bash
# OpenAI for sentiment analysis (GPT-4o-mini)
OPENAI_API_KEY=sk-proj-xxxxx

# Anthropic Claude for synthesis (Claude Sonnet 4.5)
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Google Gemini for entity extraction (Gemini 2.5 Flash)
GOOGLE_API_KEY=xxxxx

# Processing configuration
SIGNAL_PROCESSOR_BATCH_SIZE=50
SENTIMENT_BATCH_SIZE=15
```

## How to Add Variables in Railway

1. Go to your Railway dashboard
2. Select your PULSE project
3. Click on the service (backend)
4. Go to **Variables** tab
5. Click **+ New Variable**
6. Add each variable above

## Deployment Steps

1. **Commit and push the updated main.py:**
   ```bash
   git add backend/main.py backend/RAILWAY_DEPLOYMENT.md
   git commit -m "feat: integrate intelligence layer into Railway cron job"
   git push origin main
   ```

2. **Railway will auto-deploy** (if connected to GitHub)

3. **Add the new environment variables** (see above)

4. **Restart the service** in Railway dashboard

## Expected Behavior

Every 6 hours, the cron job will:
1. Scrape Reddit (7 subreddits, ~200-300 posts)
2. Save quality signals to `raw_signals` table
3. **NEW**: Process unprocessed signals through AI layer
4. **NEW**: Save insights to `insights` table

## Logs to Expect

```
================================================================================
🚀 PULSE CRON JOB - 2026-01-27 12:00:00
================================================================================

================================================================================
📡 STEP 1: SCRAPING REDDIT
================================================================================

[scraper output...]

================================================================================
✅ SCRAPING COMPLETED
================================================================================
  Scraped: 289 posts
  Quality Signals: 289
  Saved to Database: 289
================================================================================

================================================================================
🧠 STEP 2: PROCESSING SIGNALS (INTELLIGENCE LAYER)
================================================================================

[intelligence layer output...]

================================================================================
✅ INTELLIGENCE PROCESSING COMPLETED
================================================================================
  Signals Processed: 50
  Insights Generated: 8
  Tickers Extracted: 23
================================================================================

================================================================================
✅ CRON JOB COMPLETED SUCCESSFULLY
================================================================================
  Total Posts Scraped: 289
  Signals Processed: 50
  Insights Generated: 8
  Timestamp: 2026-01-27T12:05:30.123456
================================================================================
```

## Troubleshooting

### Error: "Missing required API keys"
- **Solution**: Add OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY to Railway variables

### Error: Gemini quota exceeded
- **Expected**: Gemini Layer 3 will fail gracefully, Layers 1+2 will still extract tickers
- **Solution**: This is normal on free tier, system works fine without it

### Error: "No unprocessed signals"
- **Expected**: If all signals were already processed
- **Solution**: This is normal, job completes successfully

### Intelligence layer not running
- **Check**: Make sure Railway redeployed after pushing main.py changes
- **Check**: Verify AI API keys are set in Railway environment variables

## Monitoring

1. **Check Railway logs** after each cron run (every 6 hours)
2. **Verify in Supabase**:
   - `raw_signals` table: Check `processed = TRUE` and `extracted_entities` populated
   - `insights` table: Check for new insights with timestamps

## Cost Management

- **OpenAI (GPT-4o-mini)**: ~$0.10-0.20 per 1000 signals (very cheap)
- **Anthropic (Claude Sonnet)**: ~$3-5 per 1000 signals (main cost)
- **Gemini**: Free tier sufficient (1000 requests/day)

**Estimated monthly cost**: $15-30 for typical usage (300 signals/day)

## Next Steps

After deployment:
1. Monitor first cron run in Railway logs
2. Verify insights are being created in Supabase
3. Adjust `SIGNAL_PROCESSOR_BATCH_SIZE` if needed (default: 50)
