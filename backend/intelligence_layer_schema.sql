-- ============================================================================
-- PULSE Intelligence Layer Schema
-- ============================================================================
-- Creates the insights table for Claude-synthesized market intelligence
-- Run this in Supabase SQL Editor to set up the intelligence layer database

-- Create insights table for Claude synthesis results
CREATE TABLE IF NOT EXISTS insights (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    theme VARCHAR(500) NOT NULL,
    confidence_score FLOAT NOT NULL CHECK (confidence_score >= 0 AND confidence_score <= 1),
    sources_agreeing TEXT[] DEFAULT ARRAY[]::TEXT[],
    related_assets TEXT[] DEFAULT ARRAY[]::TEXT[],
    sentiment VARCHAR(20) CHECK (sentiment IN ('bullish', 'bearish', 'neutral')),
    urgency VARCHAR(20) CHECK (urgency IN ('immediate', 'developing', 'background')),
    evidence JSONB,
    signal_ids UUID[] DEFAULT ARRAY[]::UUID[],
    created_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ
);

-- Index for querying high-confidence insights
CREATE INDEX IF NOT EXISTS idx_insights_confidence
ON insights(confidence_score DESC)
WHERE confidence_score > 0.7;

-- Index for querying by urgency
CREATE INDEX IF NOT EXISTS idx_insights_urgency
ON insights(urgency, created_at DESC);

-- Comments for documentation
COMMENT ON TABLE insights IS 'Claude-synthesized market insights from aggregated signals';
COMMENT ON COLUMN insights.confidence_score IS 'Confidence level: 0.9+=multi-source strong, 0.7-0.9=single strong, 0.5-0.7=emerging';
COMMENT ON COLUMN insights.theme IS 'Main insight theme or market narrative';
COMMENT ON COLUMN insights.sources_agreeing IS 'Array of source names/IDs that support this insight';
COMMENT ON COLUMN insights.related_assets IS 'Tickers or assets related to this insight';
COMMENT ON COLUMN insights.sentiment IS 'Overall market sentiment for this theme';
COMMENT ON COLUMN insights.urgency IS 'Time-sensitivity of this insight';
COMMENT ON COLUMN insights.evidence IS 'Supporting evidence and data points';
COMMENT ON COLUMN insights.signal_ids IS 'UUIDs of raw_signals that contributed to this insight';
COMMENT ON COLUMN insights.expires_at IS 'When this insight becomes stale (optional)';
