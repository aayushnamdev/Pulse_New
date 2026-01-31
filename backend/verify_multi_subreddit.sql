-- Run this in Supabase SQL Editor to verify multi-subreddit data

-- 1. Count posts per subreddit
SELECT
    subreddit,
    COUNT(*) as total_posts,
    COUNT(*) FILTER (WHERE is_quality_signal = TRUE) as quality_signals,
    ROUND(AVG((engagement_metrics->>'upvotes')::int), 0) as avg_upvotes
FROM raw_signals
WHERE scraped_at > NOW() - INTERVAL '1 hour'
GROUP BY subreddit
ORDER BY total_posts DESC;

-- 2. Show most recent posts from each subreddit
SELECT
    subreddit,
    title,
    engagement_metrics->>'upvotes' as upvotes,
    is_quality_signal,
    source_created_at
FROM raw_signals
WHERE scraped_at > NOW() - INTERVAL '1 hour'
ORDER BY source_created_at DESC
LIMIT 20;

-- 3. Find quality signals across all subreddits
SELECT
    subreddit,
    title,
    engagement_metrics->>'upvotes' as upvotes,
    source_created_at
FROM raw_signals
WHERE is_quality_signal = TRUE
  AND scraped_at > NOW() - INTERVAL '1 hour'
ORDER BY source_created_at DESC;
