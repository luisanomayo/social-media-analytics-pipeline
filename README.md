# Twitter Analytics Pipeline with Python, PostgreSQL & Google Sheets

This project demonstrates a data pipeline for social media analytics using Python, PostgreSQL, and Google Sheets. It retrieves tweets from a public Twitter account using the TwitterAPI.io endpoint, processes and stores them in a local PostgreSQL database, and outputs cleaned, analysis-ready data to a Google Sheet for dashboarding in Looker Studio.

![Dashboard Preview](./media/dashboard.png)

---

## 🔧 Project Structure

  ``` 
  project/ 
  ├── src/ 
  │ └── config.py # Environment and credential management 
  ├── sql/ 
  │ ├── create_raw_tables.sql 
  │ ├── create_cleaned_tweets.sql 
  │ └── create_dashboard_views.sql 
  ├── fetch_and_store_tweets.py # Ingests tweet data 
  ├── export_views_to_sheets.py # Pushes SQL views to Google Sheets 
  ├── requirements.txt 
  ├── .env 
  ├── .gitignore 
  └── README.md 
  ``` 
---

## 📊 Dashboard Metrics

The project supports a Looker Studio dashboard with:

- **Summary metrics (MoM):** Posts, impressions, engagement rate, retweets, replies, likes  
- **Time series:** Monthly impressions + 6-month rolling average  
- **Breakdowns:** content type distribution and top tweets by impressions  

---

## 🧹 Data Workflow

1. **Raw Ingestion**  
   - Only relevant fields are extracted from tweet and author payloads
   - Stored in `raw_tweets` with deduplication via `tweet_id` primary key

2. **Transformation (SQL)**  
   - Cleaned table created with additional fields like week start, engagement rate
   - Tweet type standardized (e.g. converting booleans into readable flags)

3. **Export**
   - Dashboard views created in PostgreSQL
   - Output pushed to a connected Google Sheet for Looker Studio reporting

---

## ✅ What This Project Demonstrates

- Building and testing modular Python ETL scripts
- Staging raw data before transformation (PostgreSQL)
- SQL for data cleaning, aggregation, and reporting views
- Handling credential management securely
- Documenting limitations and planning for improvement
  
---

## 🔍 Known Limitations

- Currently uses a local PostgreSQL instance (cloud migration would improve workflow, consider using AWS or GCP's Bigquery)
- Sentiment analysis and content labeling can add additional insight, considering introducing LLMs like OpenAI's ChatGPT for this
- No automated scheduling, can be extended to handle periodic tweet extraction, transformation, analytics & reporting

---

## 🚀 Future Improvements

- Migrate to GCP or hosted PostgreSQL
- Add sentiment & content type tagging with LLM APIs
- Set up automated job scheduling and retry logic
- Improve data quality checks and testing coverage

---
## 🙌 Acknowledgments

Thanks to the open APIs and tools that made this possible:
- [TwitterAPI.io](https://twitterapi.io/)
- [PostgreSQL](https://www.postgresql.org/)
- [gspread](https://gspread.readthedocs.io/en/latest/)
- [Looker Studio](https://lookerstudio.google.com/)

---

## 📄 License

MIT License  
Free to use, modify, and adapt.

---

