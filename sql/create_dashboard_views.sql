CREATE OR REPLACE VIEW v_monthly_summary AS
SELECT
    DATE_TRUNC('month', created_at) AS month,
    COUNT(*) AS post_count,
    SUM(view_count) AS impressions,
    --engagement metric
    ROUND(SUM(reply_count + retweet_count + like_count + quote_count) ::NUMERIC/NULLIF(SUM(view_count), 0) * 100, 2) AS engagement_rate,
    SUM(retweet_count + quote_count) AS shares,
    SUM(reply_count) AS replies,
    SUM(like_count) AS likes
FROM cleaned_tweets
GROUP BY month
ORDER BY month DESC;

CREATE OR REPLACE VIEW v_daily_impressions AS
SELECT
    DATE_TRUNC('day', created_at) AS day,
    SUM(view_count) AS impressions
FROM cleaned_tweets
WHERE created_at >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
GROUP BY day
ORDER BY day;

CREATE OR REPLACE VIEW v_monthly_impressions AS
SELECT
    DATE_TRUNC('month', created_at) AS month,
    SUM(view_count) AS impressions
FROM cleaned_tweets
GROUP BY month
ORDER BY month;

CREATE OR REPLACE VIEW v_rolling_avg_impressions AS
SELECT
    MONTH,
    ROUND(AVG(impressions) OVER (
        ORDER BY MONTH 
        ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
        ), 2
        )AS rolling_avg_impressions
FROM(
    SELECT
        DATE_TRUNC('month', created_at) AS month,
        SUM(view_count) AS impressions
    FROM cleaned_tweets
    GROUP BY month
) sub;

--tweet type distribution
CREATE OR REPLACE VIEW v_tweet_type_distribution AS
SELECT
    tweet_type,
    COUNT(*) AS count
FROM cleaned_tweets
GROUP BY tweet_type;

--top tweet by impressions
CREATE OR REPLACE VIEW v_top_tweets_last_month AS
SELECT
    tweet_id,
    created_at,
    view_count AS impressions,
    clean_text,
    ROUND((reply_count + quote_count + retweet_count +like_count) ::NUMERIC/NULLIF(view_count, 0) * 100, 2) AS engagement_rate
FROM cleaned_tweets
WHERE created_at >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
    AND created_at < DATE_TRUNC('month', CURRENT_DATE)
ORDER BY view_count DESC
LIMIT 5;