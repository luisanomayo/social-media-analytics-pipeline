#import libraries & modules
import os
import psycopg2
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from src.config import SERVICE_ACCOUNT_JSON, SPREADSHEET_KEY, PG_HOST, PG_PORT, PG_USER, PG_PASS, PG_DB

#define view names 
VIEWS = {
    "v_monthly_summary": "Monthly Summary",
    "v_daily_impressions": "Daily Impressions",
    "v_monthly_impressions": "Monthly Impressions",
    "v_rolling_avg_impressions": "Rolling Avg Impressions",
    "v_top_tweets_last_month": "Top Tweets",
    "v_tweet_type_distribution": "Tweet Type Distribution"
}

def connect_to_postgres():
    """Connect to PostgreSQL database."""
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        user=PG_USER,
        password=PG_PASS,
        database=PG_DB
    )
    
def connect_to_google_sheets():
    """Connect to Google Sheets using service account credentials."""
    creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_JSON,
    scopes=[
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ])
    client = gspread.authorize(creds)
    return client.open_by_key(SPREADSHEET_KEY)

def export_views_to_sheets(view_name, sheet_name,conn, spreadsheet):
    query = f"SELECT * FROM {view_name};"
    df = pd.read_sql_query(query, conn)
    
    #convert all columns to string to ensure jSON serializable
    df = df.astype(str)
    
    try:
        worksheet = spreadsheet.worksheet(sheet_name)
        worksheet.clear()  # Clear existing data
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=sheet_name, rows="100", cols="20")
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    print (f"Exported {view_name} to {sheet_name} successfully.")
    
    
def export_all_views():
    """Export all views to Google Sheets."""
    conn = connect_to_postgres()
    spreadsheet = connect_to_google_sheets()
    
    for view_name, sheet_name in VIEWS.items():
        export_views_to_sheets(view_name, sheet_name, conn, spreadsheet)
    
    conn.close()
    print("All views exported successfully.")
    
if __name__ == "__main__":
    export_all_views()
    print("Script executed successfully.")
    # This script exports PostgreSQL views to Google Sheets using service account credentials.