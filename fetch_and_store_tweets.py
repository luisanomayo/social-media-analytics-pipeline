import requests
import pandas as pd
from datetime import datetime
from src.config import (
    TWITTER_BEARER_TOKEN,
    PG_HOST, PG_PORT, PG_USER, PG_PASS, PG_DB
)
import psycopg2


# --- API request setup ---
headers = {
    "X-API-Key": TWITTER_BEARER_TOKEN
}
params = {
    "userName": "SandTechInc"
}
url = "https://api.twitterapi.io/twitter/user/last_tweets"


# --- Parse tweet payload ---
def parse_tweets(response_json):
    tweets_data = response_json.get("data", {}).get("tweets", [])
    parsed = []

    for tweet in tweets_data:
        author = tweet.get("author", {})
        parsed.append({
            "tweet_id": tweet.get("id"),
            "tweet_type": tweet.get("type"),
            "url": tweet.get("url"),
            "text": tweet.get("text"),
            "source": tweet.get("source"),
            "retweet_count": tweet.get("retweetCount"),
            "reply_count": tweet.get("replyCount"),
            "like_count": tweet.get("likeCount"),
            "quote_count": tweet.get("quoteCount"),
            "view_count": tweet.get("viewCount"),
            "created_at": tweet.get("createdAt"),
            "lang": tweet.get("lang"),
            "isreply": tweet.get("isReply"),
            "isReplyToUsername": tweet.get("inReplyToUsername"),

            # Author fields
            "author_id": author.get("id"),
            "author_username": author.get("userName"),
            "author_name": author.get("name"),
            "author_type": author.get("type"),
            "author_verified": author.get("isVerified"),
            "author_blue_verified": author.get("isBlueVerified"),
            "author_verified_type": author.get("verifiedType")
        })

    return parsed


# --- Insert parsed tweets into raw_tweets table ---
def insert_raw_tweets(tweets: list):
    conn = psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DB,
        user=PG_USER,
        password=PG_PASS
    )
    cur = conn.cursor()

    query = """
    INSERT INTO raw_tweets (
        tweet_id, tweet_type, url, text, source,
        retweet_count, reply_count, like_count, quote_count, view_count,
        created_at, lang, isreply, "isReplyToUsername",
        author_id, author_username, author_name, author_type,
        author_verified, author_blue_verified, author_verified_type
    )
    VALUES (
        %(tweet_id)s, %(tweet_type)s, %(url)s, %(text)s, %(source)s,
        %(retweet_count)s, %(reply_count)s, %(like_count)s, %(quote_count)s, %(view_count)s,
        %(created_at)s, %(lang)s, %(isreply)s, %(isReplyToUsername)s,
        %(author_id)s, %(author_username)s, %(author_name)s, %(author_type)s,
        %(author_verified)s, %(author_blue_verified)s, %(author_verified_type)s
    )
    ON CONFLICT (tweet_id) DO NOTHING;
    """

    cur.executemany(query, tweets)
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Inserted {len(tweets)} rows into raw_tweets.")


# --- Main execution ---
if __name__ == "__main__":
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        parsed_tweets = parse_tweets(response.json())
        print(f"Parsed {len(parsed_tweets)} tweets.")

        # Optional: preview
        df = pd.DataFrame(parsed_tweets)
        df['created_at'] = pd.to_datetime(df['created_at'])
        df = df.sort_values(by='created_at', ascending=False).reset_index(drop=True)
        print(df.head(3))

        insert_raw_tweets(parsed_tweets)
    else:
        print("❌ API error:", response.status_code)
