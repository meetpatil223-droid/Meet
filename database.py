import os
import sys
import sqlite3
from pathlib import Path
from dotenv import load_dotenv

# Explicitly target .env in the same folder as database.py
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = None

if SUPABASE_URL and SUPABASE_KEY:
    try:
        from supabase import create_client, Client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"[ERROR] Failed to initialize Supabase client: {str(e)}")
else:
    print("[INFO] Missing SUPABASE credentials; local SQLite will be used as database.")

DB_PATH = Path(__file__).resolve().parent / 'messages.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    try:
        with get_db() as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                subject TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_read INTEGER DEFAULT 0
            );
            """)
    except Exception as e:
        print(f"Error initializing local SQLite database: {e}")

init_db()