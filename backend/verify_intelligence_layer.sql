-- ============================================================================
-- Verification Queries for PULSE Intelligence Layer
-- ============================================================================
-- Run these in Supabase SQL Editor to verify the intelligence layer is working

-- 1. Check processed signals (should show extracted entities and sentiment scores)
SELECT
    id,
    title,
    subreddit,
    upvotes,
    extracted_entities,
    sentiment_score,
    processed,
    created_at
FROM raw_signals
WHERE processed = TRUE
ORDER BY created_at DESC
LIMIT 10;

-- 2. Check insights table (should show Claude-synthesized themes)
SELECT
    id,
    theme,
    confidence_score,
    related_assets,
    sentiment,
    urgency,
    sources_agreeing,
    array_length(signal_ids, 1) as num_signals,
    created_at
FROM insights
ORDER BY created_at DESC
LIMIT 10;

-- 3. Count processed vs unprocessed signals
SELECT
    processed,
    COUNT(*) as count
FROM raw_signals
GROUP BY processed;

-- 4. View high-confidence insights (> 0.7)
SELECT
    theme,
    confidence_score,
    related_assets,
    urgency,
    created_at
FROM insights
WHERE confidence_score > 0.7
ORDER BY confidence_score DESC;

-- 5. Count unique tickers extracted
SELECT
    jsonb_array_elements_text(extracted_entities->'tickers') as ticker,
    COUNT(*) as mentions
FROM raw_signals
WHERE processed = TRUE
  AND extracted_entities IS NOT NULL
  AND jsonb_typeof(extracted_entities->'tickers') = 'array'
GROUP BY ticker
ORDER BY mentions DESC;
