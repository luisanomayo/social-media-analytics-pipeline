from dotenv import load_dotenv
import os

#load the .env file 
load_dotenv()

#twitter API token
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

#service account credentials
SERVICE_ACCOUNT_JSON = os.getenv("SERVICE_ACCOUNT_CREDENTIALS")

#spreadsheet ID
SPREADSHEET_KEY = os.getenv("SPREADSHEET_KEY")

#PGSQL database connection
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_USER = os.getenv("PG_USER")
PG_PASS = os.getenv("PG_PASS")
PG_DB = os.getenv("PG_DB")
