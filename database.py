import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

# Explicitly target .env in the same folder as database.py
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = None

if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"❌ Failed to initialize Supabase client: {str(e)}")
else:
    print("⚠️ WARNING: Missing SUPABASE_URL or SUPABASE_KEY in environment variables.")