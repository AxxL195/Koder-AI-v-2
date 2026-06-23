import os
import hashlib
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY =  os.getenv("GEMINI_API_KEY")
GITHUB_WEBHOOK_KEY =  os.getenv("GITHUB_WEBHOOK_KEY")
PRIVATE_KEY= os.getenv("PRIVATE_KEY")
APP_ID = os.getenv("APP_ID")
SUPABASE_URL =  os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

