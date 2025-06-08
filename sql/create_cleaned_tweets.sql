DROP TABLE IF EXISTS cleaned_tweets;

CREATE TABLE cleaned_tweets AS
SELECT
    tweet_id,
    created_at,
    DATE_TRUNC('week', created_at) AS week_start,
    --clean text by removing links
    REGEXP_REPLACE(text, 'https?://[^\s]+', '', 'g') AS clean_text,
    --convert boolean to label on 'isReply'
    CASE
        WHEN isReply THEN 'Reply'
        ELSE 'Original'
    END AS tweet_type,
    -- post_level metrics with fallback to 0
    COALESCE(retweet_count, 0) AS retweet_count,
    COALESCE(reply_count, 0) AS reply_count,
    COALESCE(like_count, 0) AS like_count,
    COALESCE(quote_count, 0) AS quote_count,    
    COALESCE(view_count, 0) AS view_count,
    --language normalization
    CASE
        WHEN lang = 'en' THEN 'English'
        WHEN lang = 'en-gb' THEN 'English (UK)'
        WHEN lang = 'en-us' THEN 'English (US)'
        WHEN lang = 'es' THEN 'Spanish'
        WHEN lang = 'fr' THEN 'French'
        WHEN lang = 'de' THEN 'German'
        WHEN lang = 'it' THEN 'Italian'
        WHEN lang = 'pt' THEN 'Portuguese'
        WHEN lang = 'ja' THEN 'Japanese'
        WHEN lang = 'zh' THEN 'Chinese'
        WHEN lang = 'ar' THEN 'Arabic'
        ELSE lang
    END AS LANGUAGE,
    --author information
    author_id,
    author_username,
    author_name,
    author_verified 
FROM raw_tweets;