-- ============================================================================
-- PULSE Database Schema - raw_signals Table
-- ============================================================================
-- This table stores all incoming signals from Reddit, Polymarket, and Twitter
-- Run this in your Supabase SQL Editor to create the table
-- ============================================================================

CREATE TABLE IF NOT EXISTS raw_signals (
    -- Primary identifier
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Source information
    source VARCHAR(50) NOT NULL,              -- 'reddit', 'polymarket', 'twitter'
    source_id VARCHAR(255) UNIQUE,            -- Original post/market ID (unique to prevent duplicates)
    subreddit VARCHAR(100),                   -- For Reddit: which subreddit

    -- Content
    title TEXT,                               -- Post title (Reddit/Twitter)
    content TEXT,                             -- Post body/description
    author_id VARCHAR(255),                   -- Username/author
    author_credibility FLOAT DEFAULT 0.5,     -- Credibility score (0-1)

    -- Engagement metrics (stored as JSON for flexibility)
    engagement_metrics JSONB,                 -- {upvotes, comments, upvote_ratio, velocity}

    -- Analysis fields (populated by processing pipeline)
    extracted_entities JSONB,                 -- {tickers: [], companies: [], keywords: []}
    sentiment_score FLOAT,                    -- -1 (bearish) to 1 (bullish)
    urgency_score FLOAT,                      -- 0 to 1 (how urgent/important)

    -- Quality flags
    is_quality_signal BOOLEAN DEFAULT FALSE,  -- Contains supply chain keywords
    processed BOOLEAN DEFAULT FALSE,          -- Has this been processed by AI?

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),     -- When we saved this to DB
    source_created_at TIMESTAMPTZ,            -- When it was posted on the platform

    -- Metadata
    scraped_at TIMESTAMPTZ,                   -- When we scraped this
    age_hours FLOAT                           -- Age of post when scraped
);

-- ============================================================================
-- INDEXES for Performance
-- ============================================================================

-- Index on source_id for duplicate checking
CREATE INDEX IF NOT EXISTS idx_raw_signals_source_id
ON raw_signals(source_id);

-- Index on source and created_at for filtering by platform and time
CREATE INDEX IF NOT EXISTS idx_raw_signals_source_created
ON raw_signals(source, source_created_at DESC);

-- Index on is_quality_signal for filtering high-value signals
CREATE INDEX IF NOT EXISTS idx_raw_signals_quality
ON raw_signals(is_quality_signal)
WHERE is_quality_signal = TRUE;

-- Index on processed flag for pipeline processing
CREATE INDEX IF NOT EXISTS idx_raw_signals_processed
ON raw_signals(processed)
WHERE processed = FALSE;

-- ============================================================================
-- COMMENTS for Documentation
-- ============================================================================

COMMENT ON TABLE raw_signals IS 'Stores all incoming signals from social platforms before AI processing';
COMMENT ON COLUMN raw_signals.source IS 'Platform: reddit, polymarket, or twitter';
COMMENT ON COLUMN raw_signals.source_id IS 'Unique ID from the source platform (prevents duplicate scraping)';
COMMENT ON COLUMN raw_signals.engagement_metrics IS 'JSON with upvotes, comments, upvote_ratio, velocity, etc.';
COMMENT ON COLUMN raw_signals.extracted_entities IS 'JSON with tickers, companies, keywords extracted from content';
COMMENT ON COLUMN raw_signals.is_quality_signal IS 'TRUE if contains supply chain keywords (delay, shortage, etc.)';
COMMENT ON COLUMN raw_signals.processed IS 'TRUE after Claude AI has analyzed this signal';

-- ============================================================================
-- SAMPLE QUERY: View Recent Quality Signals
-- ============================================================================

-- Uncomment to test after inserting data:
-- SELECT
--     title,
--     source,
--     engagement_metrics->>'upvotes' as upvotes,
--     engagement_metrics->>'velocity' as velocity,
--     is_quality_signal,
--     source_created_at
-- FROM raw_signals
-- WHERE is_quality_signal = TRUE
-- ORDER BY source_created_at DESC
-- LIMIT 10;
