# 🚀 PULSE Backend - Setup Guide

This is the backend scraper service for PULSE that harvests Reddit signals and stores them in Supabase.

## 📋 What's Inside

```
backend/
├── main.py                 # Railway cron job entry point
├── scraper_service.py      # Reddit scraper (core logic)
├── database_service.py     # Supabase connection & storage
├── schema.sql              # Database table schema
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── .env                    # Your actual credentials (DO NOT COMMIT)
└── .gitignore              # Protects sensitive files
```

---

## 🛠️ Local Setup (Development)

### Step 1: Create Supabase Project

1. Go to [https://app.supabase.com](https://app.supabase.com)
2. Create a new project (choose a region close to you)
3. Wait for the project to spin up (~2 minutes)

### Step 2: Run the Database Schema

1. In Supabase, go to **SQL Editor**
2. Open `schema.sql` from this folder
3. Copy the entire contents
4. Paste into Supabase SQL Editor and click **Run**
5. Verify the `raw_signals` table was created (check **Table Editor**)

### Step 3: Get Your Supabase Credentials

1. In Supabase, go to **Settings** → **API**
2. Copy:
   - **Project URL** (looks like `https://xxxxx.supabase.co`)
   - **anon/public key** (the `anon` key, NOT the service_role key)

### Step 4: Configure Environment Variables

1. Open `.env` file in this folder
2. Fill in your credentials:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here

REDDIT_FETCH_LIMIT=100
REDDIT_SUBREDDIT=wallstreetbets
MIN_UPVOTE_RATIO=0.70
MIN_UPVOTES=50
ENVIRONMENT=development
```

### Step 5: Install Dependencies

```bash
# Make sure you're in the backend folder
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 6: Test Everything

**Test 1: Database Connection**
```bash
python database_service.py
```
You should see:
- ✅ Connected to Supabase
- Database stats
- Test insert successful

**Test 2: Scraper (without DB)**
```bash
python scraper_service.py
```
You should see:
- List of scraped posts
- Quality signals flagged
- Results saved to `test_scraper_output.json`

**Test 3: Full Pipeline (scraper + database)**
```bash
# In Python console:
python
>>> from scraper_service import RedditScraper
>>> scraper = RedditScraper()
>>> result = scraper.run(save_to_db=True)
```

Check Supabase Table Editor - you should see new rows in `raw_signals`!

---

## 🚂 Railway Deployment (Production)

### Step 1: Push to GitHub

```bash
# Initialize git (if not already done)
cd /path/to/Pulse
git init

# Add all files
git add .

# Commit
git commit -m "Initial PULSE backend setup"

# Create GitHub repo and push
# (Follow GitHub instructions to create repo and push)
```

### Step 2: Deploy to Railway

1. Go to [https://railway.app](https://railway.app)
2. Click **New Project** → **Deploy from GitHub repo**
3. Select your Pulse repository
4. Railway will auto-detect Python and deploy

### Step 3: Configure Railway Environment Variables

In Railway dashboard:

1. Go to your project → **Variables** tab
2. Add these variables:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
REDDIT_FETCH_LIMIT=100
REDDIT_SUBREDDIT=wallstreetbets
MIN_UPVOTE_RATIO=0.70
MIN_UPVOTES=50
ENVIRONMENT=production
```

### Step 4: Set Up Cron Job

1. In Railway, go to **Settings**
2. Find **Cron Schedule** section
3. Enter: `0 */6 * * *`
   - This runs every 6 hours: 12am, 6am, 12pm, 6pm UTC
4. Set **Cron Command**: `python main.py`
5. Save

### Step 5: Test Deployment

Click **Deploy** in Railway and watch the logs. You should see:
- ✅ Connected to Supabase
- ✅ Scraped X posts
- ✅ Saved to database

---

## 📊 Monitoring & Verification

### Check if it's working:

**Option 1: Railway Logs**
- Go to Railway dashboard → **Deployments** → **View Logs**
- Look for "CRON JOB COMPLETED SUCCESSFULLY"

**Option 2: Supabase Dashboard**
- Go to Supabase → **Table Editor** → `raw_signals`
- Check the timestamps - should have new data every 6 hours

**Option 3: SQL Query**
```sql
-- Run in Supabase SQL Editor
SELECT
    COUNT(*) as total_signals,
    COUNT(*) FILTER (WHERE is_quality_signal = TRUE) as quality_signals,
    MAX(scraped_at) as last_scrape
FROM raw_signals;
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'requests'"
**Fix:** Make sure virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Missing Supabase credentials"
**Fix:** Double-check your `.env` file has valid `SUPABASE_URL` and `SUPABASE_KEY`

### "Table 'raw_signals' does not exist"
**Fix:** Run the `schema.sql` file in Supabase SQL Editor

### Railway cron job not running
**Fix:**
1. Verify cron schedule: `0 */6 * * *`
2. Verify cron command: `python main.py`
3. Check environment variables are set in Railway
4. Check Railway logs for errors

### No data showing in Supabase
**Fix:**
1. Test locally first: `python scraper_service.py`
2. Check Reddit is accessible (not blocked)
3. Verify filters aren't too strict (lower `MIN_UPVOTES` temporarily)

---

## 🎯 Next Steps

Once your scraper is running:

1. **Monitor Data Quality** - Check if the quality signals are accurate
2. **Adjust Filters** - Tune `MIN_UPVOTE_RATIO` and `MIN_UPVOTES` based on results
3. **Add More Keywords** - Edit `quality_keywords` in `scraper_service.py`
4. **Phase 2** - Add Polymarket integration
5. **Phase 3** - Build the AI synthesis layer with Claude

---

## 📝 Configuration Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `SUPABASE_URL` | (required) | Your Supabase project URL |
| `SUPABASE_KEY` | (required) | Your Supabase anon key |
| `REDDIT_FETCH_LIMIT` | 100 | How many posts to fetch |
| `REDDIT_SUBREDDIT` | wallstreetbets | Which subreddit to scrape |
| `MIN_UPVOTE_RATIO` | 0.70 | Minimum upvote ratio (70%) |
| `MIN_UPVOTES` | 50 | Minimum upvotes required |
| `ENVIRONMENT` | development | Set to `production` on Railway |

---

## 📞 Need Help?

Refer to:
- Main blueprint: `/PULSE_Project_Blueprint.md`
- Database schema: `schema.sql`
- Example output: `test_scraper_output.json`

---

**Built with ❤️ by Aayush for PULSE**
