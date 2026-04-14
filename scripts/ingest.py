"""
ingest.py
---------
Fetches news from NewsAPI, cleans data with pandas,
runs NLP analysis, and stores everything in MySQL.

Run manually:    python scripts/ingest.py
Run on schedule: python scripts/scheduler.py
"""

import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os
import sys

# Allow imports from the scripts folder
sys.path.append(os.path.dirname(__file__))
from db_connection import get_connection
from nlp_analysis import analyse_article

load_dotenv()

# ── Configuration ─────────────────────────────────────────────────────────────
API_KEY   = os.getenv("NEWS_API_KEY")
BASE_URL  = "https://newsapi.org/v2/top-headlines"

# Countries and categories to fetch
COUNTRIES   = ["us", "in", "gb", "au", "ca"]
CATEGORIES  = ["business", "technology", "health", "science", "sports", "entertainment", "general"]

COUNTRY_NAMES = {
    "us": "United States", "in": "India", "gb": "United Kingdom",
    "au": "Australia",     "ca": "Canada"
}


# ── Step 1: Fetch raw articles from NewsAPI ───────────────────────────────────
def fetch_articles() -> pd.DataFrame:
    """
    Calls NewsAPI for each country+category combination.
    Returns a single pandas DataFrame of all raw articles.
    """
    all_articles = []

    for country in COUNTRIES:
        for category in CATEGORIES:
            try:
                response = requests.get(
                    BASE_URL,
                    params={
                        "country":  country,
                        "category": category,
                        "pageSize": 20,
                        "apiKey":   API_KEY
                    },
                    timeout=10
                )

                if response.status_code != 200:
                    print(f"  ⚠️  API error for {country}/{category}: {response.status_code}")
                    continue

                data = response.json()
                articles = data.get("articles", [])

                for article in articles:
                    all_articles.append({
                        "title":        article.get("title", ""),
                        "description":  article.get("description", ""),
                        "source_name":  article.get("source", {}).get("name", "Unknown"),
                        "url":          article.get("url", ""),
                        "published_at": article.get("publishedAt", ""),
                        "country":      country,
                        "category":     category
                    })

            except requests.exceptions.RequestException as e:
                print(f"  ❌ Network error for {country}/{category}: {e}")
                continue

    print(f"  📥 Fetched {len(all_articles)} raw articles from API.")
    return pd.DataFrame(all_articles)


# ── Step 2: Clean data using pandas ──────────────────────────────────────────
def clean_articles(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the raw DataFrame:
    - Drops rows with missing title or url
    - Removes duplicate URLs
    - Cleans text (strips whitespace, removes [Removed] placeholders)
    - Parses published_at into proper datetime
    - Drops articles with no meaningful content
    """
    if df.empty:
        return df

    # Drop rows with missing essential fields
    df = df.dropna(subset=["title", "url"])

    # Remove placeholder articles NewsAPI sometimes returns
    df = df[df["title"] != "[Removed]"]
    df = df[df["url"]   != "https://removed.com"]

    # Strip whitespace from text columns
    df["title"]       = df["title"].str.strip()
    df["description"] = df["description"].fillna("").str.strip()
    df["source_name"] = df["source_name"].str.strip()

    # Remove rows where title is very short (likely junk)
    df = df[df["title"].str.len() > 10]

    # Parse published_at — handle multiple formats safely
    df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce", utc=True)
    df["published_at"] = df["published_at"].dt.tz_localize(None)  # remove timezone for MySQL

    # Drop rows where date couldn't be parsed
    df = df.dropna(subset=["published_at"])

    # Deduplicate within this batch by URL
    df = df.drop_duplicates(subset=["url"])

    # Trim URL length to avoid MySQL VARCHAR overflow
    df["url"] = df["url"].str[:700]

    print(f"  🧹 After cleaning: {len(df)} articles remain.")
    return df.reset_index(drop=True)


# ── Step 3: Insert articles into MySQL (skip duplicates) ─────────────────────
def insert_articles(df: pd.DataFrame) -> list:
    """
    Inserts cleaned articles into the 'articles' table.
    Skips URLs that already exist (deduplication via IGNORE).
    Returns list of newly inserted article IDs with their titles/descriptions.
    """
    if df.empty:
        return []

    conn   = get_connection()
    cursor = conn.cursor()

    inserted = []

    for _, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT IGNORE INTO articles
                    (title, description, source_name, country, category, url, published_at)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s)
            """, (
                row["title"],
                row["description"],
                row["source_name"],
                row["country"],
                row["category"],
                row["url"],
                row["published_at"].strftime("%Y-%m-%d %H:%M:%S")
            ))

            # If a row was actually inserted (not skipped), get its ID
            if cursor.rowcount == 1:
                inserted.append({
                    "id":          cursor.lastrowid,
                    "title":       row["title"],
                    "description": row["description"]
                })

        except Exception as e:
            print(f"  ⚠️  Skipping article due to error: {e}")
            continue

    conn.commit()
    cursor.close()
    conn.close()

    print(f"  💾 Inserted {len(inserted)} new articles into MySQL.")
    return inserted


# ── Step 4: Run NLP and insert into article_sentiment ────────────────────────
def insert_sentiment(new_articles: list):
    """
    Runs NLP analysis on newly inserted articles.
    Stores results in the article_sentiment table.
    """
    if not new_articles:
        print("  ℹ️  No new articles to analyse.")
        return

    conn   = get_connection()
    cursor = conn.cursor()

    for article in new_articles:
        result = analyse_article(article["title"], article["description"])

        cursor.execute("""
            INSERT INTO article_sentiment
                (article_id, sentiment, score, keywords, topic)
            VALUES
                (%s, %s, %s, %s, %s)
        """, (
            article["id"],
            result["sentiment"],
            result["score"],
            result["keywords"],
            result["topic"]
        ))

    conn.commit()
    cursor.close()
    conn.close()

    print(f"  🧠 NLP complete for {len(new_articles)} articles.")


# ── Step 5: Update hourly trends snapshot ────────────────────────────────────
def update_hourly_trends():
    """
    Aggregates article counts + avg sentiment per topic for the last hour.
    Inserts a fresh snapshot row into hourly_trends.
    """
    conn   = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            s.topic,
            COUNT(*)        AS article_count,
            AVG(s.score)    AS avg_sentiment,
            GROUP_CONCAT(s.keywords ORDER BY s.score DESC SEPARATOR ' | ') AS top_keywords
        FROM articles a
        JOIN article_sentiment s ON a.id = s.article_id
        WHERE a.fetched_at >= NOW() - INTERVAL 1 HOUR
        GROUP BY s.topic
    """)

    rows = cursor.fetchall()

    insert_cursor = conn.cursor()
    for row in rows:
        insert_cursor.execute("""
            INSERT INTO hourly_trends
                (snapshot_time, topic, article_count, avg_sentiment, top_keywords)
            VALUES
                (NOW(), %s, %s, %s, %s)
        """, (
            row["topic"],
            row["article_count"],
            float(row["avg_sentiment"]) if row["avg_sentiment"] else 0.0,
            row["top_keywords"]
        ))

    conn.commit()
    insert_cursor.close()
    cursor.close()
    conn.close()

    print(f"  📊 Hourly trends snapshot saved ({len(rows)} topics).")


# ── Main pipeline ─────────────────────────────────────────────────────────────
def run_pipeline():
    print(f"\n{'='*55}")
    print(f"News Pulse Ingestion — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*55}")

    raw_df        = fetch_articles()
    clean_df      = clean_articles(raw_df)
    new_articles  = insert_articles(clean_df)
    insert_sentiment(new_articles)
    update_hourly_trends()

    print(f"\nPipeline complete.\n")


if __name__ == "__main__":
    run_pipeline()
