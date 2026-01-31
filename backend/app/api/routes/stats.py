"""
PULSE Stats API
===============
FastAPI routes for dashboard statistics and analytics.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, List
from datetime import datetime, timedelta
import os
from supabase import create_client, Client

router = APIRouter()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY environment variables")

supabase: Client = create_client(supabase_url, supabase_key)


@router.get("/stats")
async def get_stats() -> Dict:
    """
    Get comprehensive dashboard statistics.

    Returns:
    {
        "total_signals": 1250,
        "total_insights": 42,
        "signals_24h": 87,
        "insights_24h": 5,
        "quality_signals": 312,
        "top_tickers": [
            {"ticker": "NVDA", "mention_count": 45},
            {"ticker": "TSLA", "mention_count": 32},
            ...
        ],
        "avg_confidence": 0.78,
        "sentiment_distribution": {
            "bullish": 18,
            "bearish": 12,
            "neutral": 12
        },
        "active_subreddits": [
            {"subreddit": "stocks", "signal_count": 250},
            {"subreddit": "investing", "signal_count": 180},
            ...
        ],
        "last_scrape": "2026-02-01T01:11:20.845632",
        "last_insight": "2026-02-01T01:12:39.278000"
    }
    """
    try:
        # Calculate 24h cutoff
        cutoff_24h = (datetime.now() - timedelta(hours=24)).isoformat()

        # Get total signals
        total_signals_response = supabase.table('raw_signals').select('id', count='exact').execute()
        total_signals = total_signals_response.count or 0

        # Get total insights
        total_insights_response = supabase.table('insights').select('id', count='exact').execute()
        total_insights = total_insights_response.count or 0

        # Get signals in last 24h
        signals_24h_response = (
            supabase.table('raw_signals')
            .select('id', count='exact')
            .gte('scraped_at', cutoff_24h)
            .execute()
        )
        signals_24h = signals_24h_response.count or 0

        # Get insights in last 24h
        insights_24h_response = (
            supabase.table('insights')
            .select('id', count='exact')
            .gte('created_at', cutoff_24h)
            .execute()
        )
        insights_24h = insights_24h_response.count or 0

        # Get quality signals count
        quality_signals_response = (
            supabase.table('raw_signals')
            .select('id', count='exact')
            .eq('is_quality_signal', True)
            .execute()
        )
        quality_signals = quality_signals_response.count or 0

        # Get average confidence score
        insights_response = supabase.table('insights').select('confidence_score').execute()
        insights_data = insights_response.data
        avg_confidence = 0.0
        if insights_data:
            avg_confidence = sum(i.get('confidence_score', 0) for i in insights_data) / len(insights_data)

        # Get sentiment distribution
        sentiment_dist = {"bullish": 0, "bearish": 0, "neutral": 0}
        for insight in insights_data:
            sentiment = insight.get('sentiment', 'neutral')
            if sentiment in sentiment_dist:
                sentiment_dist[sentiment] += 1

        # Get top tickers from signals
        signals_with_entities = (
            supabase.table('raw_signals')
            .select('extracted_entities')
            .not_.is_('extracted_entities', 'null')
            .execute()
        )

        ticker_counts = {}
        for signal in signals_with_entities.data:
            entities = signal.get('extracted_entities', {})
            tickers = entities.get('tickers', [])
            for ticker in tickers:
                ticker_counts[ticker] = ticker_counts.get(ticker, 0) + 1

        top_tickers = [
            {"ticker": ticker, "mention_count": count}
            for ticker, count in sorted(ticker_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        ]

        # Get active subreddits
        subreddit_counts_response = (
            supabase.table('raw_signals')
            .select('subreddit')
            .execute()
        )

        subreddit_counts = {}
        for signal in subreddit_counts_response.data:
            subreddit = signal.get('subreddit', 'unknown')
            subreddit_counts[subreddit] = subreddit_counts.get(subreddit, 0) + 1

        active_subreddits = [
            {"subreddit": subreddit, "signal_count": count}
            for subreddit, count in sorted(subreddit_counts.items(), key=lambda x: x[1], reverse=True)
        ]

        # Get last scrape time
        last_scrape_response = (
            supabase.table('raw_signals')
            .select('scraped_at')
            .order('scraped_at', desc=True)
            .limit(1)
            .execute()
        )
        last_scrape = last_scrape_response.data[0]['scraped_at'] if last_scrape_response.data else None

        # Get last insight time
        last_insight_response = (
            supabase.table('insights')
            .select('created_at')
            .order('created_at', desc=True)
            .limit(1)
            .execute()
        )
        last_insight = last_insight_response.data[0]['created_at'] if last_insight_response.data else None

        return {
            "total_signals": total_signals,
            "total_insights": total_insights,
            "signals_24h": signals_24h,
            "insights_24h": insights_24h,
            "quality_signals": quality_signals,
            "top_tickers": top_tickers,
            "avg_confidence": round(avg_confidence, 2),
            "sentiment_distribution": sentiment_dist,
            "active_subreddits": active_subreddits,
            "last_scrape": last_scrape,
            "last_insight": last_insight
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch stats: {str(e)}")


@router.get("/stats/tickers")
async def get_ticker_stats() -> Dict:
    """
    Get detailed statistics about tracked tickers.

    Returns top tickers with mention counts, sentiment, and recent insights.
    """
    try:
        # Get all signals with extracted entities
        signals_response = (
            supabase.table('raw_signals')
            .select('extracted_entities, sentiment_score')
            .not_.is_('extracted_entities', 'null')
            .execute()
        )

        ticker_data = {}

        for signal in signals_response.data:
            entities = signal.get('extracted_entities', {})
            tickers = entities.get('tickers', [])
            sentiment = signal.get('sentiment_score', 0.0)

            for ticker in tickers:
                if ticker not in ticker_data:
                    ticker_data[ticker] = {
                        "ticker": ticker,
                        "mention_count": 0,
                        "avg_sentiment": 0.0,
                        "sentiment_sum": 0.0
                    }

                ticker_data[ticker]["mention_count"] += 1
                ticker_data[ticker]["sentiment_sum"] += sentiment

        # Calculate average sentiment
        ticker_stats = []
        for ticker, data in ticker_data.items():
            avg_sentiment = data["sentiment_sum"] / data["mention_count"] if data["mention_count"] > 0 else 0.0
            ticker_stats.append({
                "ticker": ticker,
                "mention_count": data["mention_count"],
                "avg_sentiment": round(avg_sentiment, 2)
            })

        # Sort by mention count
        ticker_stats.sort(key=lambda x: x["mention_count"], reverse=True)

        return {
            "tickers": ticker_stats[:20],  # Top 20 tickers
            "total_tickers": len(ticker_stats)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch ticker stats: {str(e)}")
