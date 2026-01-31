"""
PULSE Insights API
==================
FastAPI routes for fetching market insights from the intelligence layer.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Optional
from datetime import datetime
import os
from supabase import create_client, Client

router = APIRouter()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY environment variables")

supabase: Client = create_client(supabase_url, supabase_key)


@router.get("/insights")
async def get_insights(
    limit: int = Query(10, ge=1, le=100, description="Number of insights to return"),
    offset: int = Query(0, ge=0, description="Number of insights to skip"),
    min_confidence: float = Query(0.7, ge=0.0, le=1.0, description="Minimum confidence score"),
    sentiment: Optional[str] = Query(None, description="Filter by sentiment: bullish, bearish, neutral")
) -> Dict:
    """
    Fetch top insights with high confidence scores.

    Returns insights sorted by created_at DESC (most recent first).
    Each insight includes theme, confidence score, related assets, sentiment, and evidence.

    Query Parameters:
    - limit: Maximum number of insights to return (default: 10, max: 100)
    - offset: Number of insights to skip for pagination (default: 0)
    - min_confidence: Minimum confidence score filter (default: 0.7)
    - sentiment: Optional sentiment filter (bullish, bearish, neutral)

    Returns:
    {
        "insights": [...],
        "total": 42,
        "limit": 10,
        "offset": 0
    }
    """
    try:
        # Build query
        query = supabase.table('insights').select('*', count='exact')

        # Apply filters
        query = query.gte('confidence_score', min_confidence)

        if sentiment:
            query = query.eq('sentiment', sentiment.lower())

        # Order by created_at DESC and apply pagination
        query = query.order('created_at', desc=True).range(offset, offset + limit - 1)

        # Execute query
        response = query.execute()

        return {
            "insights": response.data,
            "total": response.count if response.count else len(response.data),
            "limit": limit,
            "offset": offset
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch insights: {str(e)}")


@router.get("/insights/{insight_id}")
async def get_insight_by_id(insight_id: str) -> Dict:
    """
    Fetch a single insight by its ID.

    Returns detailed insight information including supporting signals.
    """
    try:
        response = supabase.table('insights').select('*').eq('id', insight_id).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Insight not found")

        return response.data[0]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch insight: {str(e)}")


@router.get("/insights/asset/{symbol}")
async def get_insights_by_asset(
    symbol: str,
    limit: int = Query(10, ge=1, le=100, description="Number of insights to return"),
    offset: int = Query(0, ge=0, description="Number of insights to skip")
) -> Dict:
    """
    Fetch insights related to a specific asset (ticker symbol).

    Returns insights where the asset appears in related_assets array.
    """
    try:
        # Query insights where related_assets contains the symbol
        query = (
            supabase.table('insights')
            .select('*', count='exact')
            .contains('related_assets', [symbol.upper()])
            .order('created_at', desc=True)
            .range(offset, offset + limit - 1)
        )

        response = query.execute()

        return {
            "insights": response.data,
            "asset": symbol.upper(),
            "total": response.count if response.count else len(response.data),
            "limit": limit,
            "offset": offset
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch insights for {symbol}: {str(e)}")
