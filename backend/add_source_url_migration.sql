-- ============================================================================
-- Migration: Add source_url column to raw_signals table
-- ============================================================================
-- Run this in your Supabase SQL Editor to add the source_url field
-- ============================================================================

-- Add source_url column to store the full URL of the source post
ALTER TABLE raw_signals
ADD COLUMN IF NOT EXISTS source_url TEXT;

-- Add comment for documentation
COMMENT ON COLUMN raw_signals.source_url IS 'Full URL to the original post (e.g., https://reddit.com/r/wallstreetbets/comments/...)';

-- Optional: Create an index if you plan to query by source_url frequently
-- CREATE INDEX IF NOT EXISTS idx_raw_signals_source_url ON raw_signals(source_url);

-- Verify the column was added
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'raw_signals' AND column_name = 'source_url';
