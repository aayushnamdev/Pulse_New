"""
PULSE Signals API
=================
FastAPI routes for fetching raw Reddit signals.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Optional
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


@router.get("/signals")
async def get_signals(
    limit: int = Query(20, ge=1, le=100, description="Number of signals to return"),
    offset: int = Query(0, ge=0, description="Number of signals to skip"),
    is_quality_signal: Optional[bool] = Query(None, description="Filter by quality signal status"),
    subreddit: Optional[str] = Query(None, description="Filter by subreddit"),
    hours: Optional[int] = Query(None, ge=1, le=168, description="Only show signals from last N hours")
) -> Dict:
    """
    Fetch recent Reddit signals.

    Returns signals sorted by scraped_at DESC (most recent first).
    Each signal includes title, content, engagement metrics, and extracted entities.

    Query Parameters:
    - limit: Maximum number of signals to return (default: 20, max: 100)
    - offset: Number of signals to skip for pagination (default: 0)
    - is_quality_signal: Filter for quality signals only (optional)
    - subreddit: Filter by specific subreddit (optional)
    - hours: Only show signals from last N hours (optional, max: 168 = 7 days)

    Returns:
    {
        "signals": [...],
        "total": 100,
        "limit": 20,
        "offset": 0
    }
    """
    try:
        # Build query
        query = supabase.table('raw_signals').select('*', count='exact')

        # Apply filters
        if is_quality_signal is not None:
            query = query.eq('is_quality_signal', is_quality_signal)

        if subreddit:
            query = query.eq('subreddit', subreddit.lower())

        if hours:
            cutoff_time = (datetime.now() - timedelta(hours=hours)).isoformat()
            query = query.gte('scraped_at', cutoff_time)

        # Order by scraped_at DESC and apply pagination
        query = query.order('scraped_at', desc=True).range(offset, offset + limit - 1)

        # Execute query
        response = query.execute()

        return {
            "signals": response.data,
            "total": response.count if response.count else len(response.data),
            "limit": limit,
            "offset": offset,
            "filters": {
                "is_quality_signal": is_quality_signal,
                "subreddit": subreddit,
                "hours": hours
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch signals: {str(e)}")


@router.get("/signals/{signal_id}")
async def get_signal_by_id(signal_id: str) -> Dict:
    """
    Fetch a single signal by its ID.

    Returns detailed signal information including full content and metadata.
    """
    try:
        response = supabase.table('raw_signals').select('*').eq('id', signal_id).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Signal not found")

        return response.data[0]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch signal: {str(e)}")


@router.get("/signals/subreddit/{subreddit}")
async def get_signals_by_subreddit(
    subreddit: str,
    limit: int = Query(20, ge=1, le=100, description="Number of signals to return"),
    offset: int = Query(0, ge=0, description="Number of signals to skip")
) -> Dict:
    """
    Fetch signals from a specific subreddit.

    Returns signals sorted by scraped_at DESC.
    """
    try:
        query = (
            supabase.table('raw_signals')
            .select('*', count='exact')
            .eq('subreddit', subreddit.lower())
            .order('scraped_at', desc=True)
            .range(offset, offset + limit - 1)
        )

        response = query.execute()

        return {
            "signals": response.data,
            "subreddit": subreddit.lower(),
            "total": response.count if response.count else len(response.data),
            "limit": limit,
            "offset": offset
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch signals for r/{subreddit}: {str(e)}")
