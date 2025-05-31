from dotenv import load_dotenv
import os

#load the .env file 
load_dotenv()

#twitter API token
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

#service account credentials
SERVICE_ACCOUNT_JSON = os.getenv("SERVICE_ACCOUNT_CREDENTIALS")