-- Active: 1749329170628@@127.0.0.1@5432@sandtech
CREATE TABLE raw_tweets (
    tweet_id BIGINT PRIMARY KEY,
    tweet_type TEXT NOT NULL,
    url TEXT NOT NULL,
    text TEXT NOT NULL,
    source TEXT,
    retweet_count INT CHECK (retweet_count >= 0),
    reply_count INT CHECK (reply_count >= 0),
    like_count INT CHECK (like_count >= 0),
    quote_count INT CHECK (quote_count >= 0),
    view_count INT CHECK (view_count >= 0),
    created_at TIMESTAMP NOT NULL,
    lang TEXT,
    isReply BOOLEAN NOT NULL,
    isRelyToUsername TEXT,
    
    author_id BIGINT,
    author_username TEXT,
    author_name TEXT,
    author_type TEXT,
    author_verified BOOLEAN,
    author_blue_verified BOOLEAN,
    author_verified_type TEXT,

    inserted_at TIMESTAMP DEFAULT now()
);
