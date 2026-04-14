"""
db_connection.py
----------------
Shared helper to get a MySQL connection.
Imported by all other scripts.
"""

import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    """Returns a live MySQL connection to the news_pulse database."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "news_pulse"),
        charset="utf8mb4"
    )
