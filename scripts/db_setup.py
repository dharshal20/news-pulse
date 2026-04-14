"""
db_setup.py
-----------
Run this ONCE to create the MySQL database and all tables.
Command: python scripts/db_setup.py
"""

import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# ── Step 1: Connect WITHOUT selecting a database (to create it) ──────────────
def get_root_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "")
    )

# ── Step 2: Connect WITH the database selected ───────────────────────────────
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "news_pulse")
    )

def create_database():
    conn = get_root_connection()
    cursor = conn.cursor()
    db_name = os.getenv("DB_NAME", "news_pulse")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    print(f"✅ Database '{db_name}' created (or already exists).")
    cursor.close()
    conn.close()

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # ── Table 1: Raw articles ─────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id            INT AUTO_INCREMENT PRIMARY KEY,
            title         TEXT NOT NULL,
            description   TEXT,
            source_name   VARCHAR(150),
            country       VARCHAR(10),
            category      VARCHAR(50),
            url           VARCHAR(700) UNIQUE,
            published_at  DATETIME,
            fetched_at    DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)
    print("✅ Table 'articles' created.")

    # ── Table 2: NLP results ──────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS article_sentiment (
            id            INT AUTO_INCREMENT PRIMARY KEY,
            article_id    INT NOT NULL,
            sentiment     VARCHAR(10),
            score         FLOAT,
            keywords      TEXT,
            topic         VARCHAR(60),
            FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)
    print("✅ Table 'article_sentiment' created.")

    # ── Table 3: Hourly trend snapshots ──────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hourly_trends (
            id              INT AUTO_INCREMENT PRIMARY KEY,
            snapshot_time   DATETIME DEFAULT CURRENT_TIMESTAMP,
            topic           VARCHAR(60),
            article_count   INT,
            avg_sentiment   FLOAT,
            top_keywords    TEXT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)
    print("✅ Table 'hourly_trends' created.")

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    print("\n🔧 Setting up News Pulse database...\n")
    create_database()
    create_tables()
    print("\n🎉 Database setup complete! You can now run the ingestion script.\n")
