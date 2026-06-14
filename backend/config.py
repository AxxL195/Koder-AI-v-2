import os
import hashlib
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY =  os.getenv("GEMINI_API_KEY")
GITHUB_WEBHOOK_KEY =  os.getenv("GITHUB_WEBHOOK_KEY")
PRIVATE_KEY= os.getenv("PRIVATE_KEY")
APP_ID = os.getenv("APP_ID")

