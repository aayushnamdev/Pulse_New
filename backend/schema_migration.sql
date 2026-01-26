-- ============================================================================
-- PULSE Schema Migration - Add Missing Columns to raw_signals
-- ============================================================================
-- Run this in Supabase SQL Editor to update your existing table
-- ============================================================================

-- Add missing columns to raw_signals table
ALTER TABLE raw_signals
  ADD COLUMN IF NOT EXISTS subreddit VARCHAR(100),
  ADD COLUMN IF NOT EXISTS title TEXT,
  ADD COLUMN IF NOT EXISTS is_quality_signal BOOLEAN DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS scraped_at TIMESTAMPTZ,
  ADD COLUMN IF NOT EXISTS age_hours FLOAT;

-- Add UNIQUE constraint to source_id (prevents duplicate scraping)
ALTER TABLE raw_signals
  ADD CONSTRAINT raw_signals_source_id_unique UNIQUE (source_id);

-- ============================================================================
-- CREATE INDEXES for Performance
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

-- Index on subreddit for filtering by community
CREATE INDEX IF NOT EXISTS idx_raw_signals_subreddit
ON raw_signals(subreddit);

-- ============================================================================
-- VERIFY THE MIGRATION
-- ============================================================================

-- Run this to check all columns exist:
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'raw_signals'
ORDER BY ordinal_position;

-- You should see all these columns:
-- id, source, source_id, content, author_id, author_credibility,
-- engagement_metrics, extracted_entities, sentiment_score, urgency_score,
-- created_at, source_created_at, processed, subreddit, title,
-- is_quality_signal, scraped_at, age_hours

-- ============================================================================
-- TEST QUERY - See your quality signals
-- ============================================================================

-- After scraper runs, use this to check quality signals:
-- SELECT
--     title,
--     subreddit,
--     engagement_metrics->>'upvotes' as upvotes,
--     engagement_metrics->>'velocity' as velocity,
--     is_quality_signal,
--     source_created_at
-- FROM raw_signals
-- WHERE is_quality_signal = TRUE
-- ORDER BY source_created_at DESC
-- LIMIT 10;
