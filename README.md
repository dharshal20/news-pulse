# ◆ News Pulse

> A real-time global news sentiment tracker — ingests live articles, runs NLP analysis, and visualises 24-hour sentiment trends in a dark, editorial-style dashboard.

##  What It Does

News Pulse pulls live articles from multiple countries via the NewsAPI, runs sentiment and keyword analysis on each one, stores everything in a normalised MySQL database, and displays the results in a Streamlit dashboard that auto-refreshes every 30 minutes.

The dashboard gives you a real-time pulse on what the world is talking about — and whether the tone is positive, negative, or neutral.

## Features

- 📡 **Live ingestion** — fetches hundreds of articles across countries via REST API, cleans and deduplicates with pandas before storing
- 🧠 **NLP pipeline** — sentiment scoring (positive / negative / neutral), keyword extraction, and topic classification on every article
- 🗄️ **Normalised MySQL schema** — articles, sentiment scores, and hourly trend snapshots stored across relational tables
- 📊 **Sentiment Timeline** — area chart showing positive vs. negative trends over the last 6–24 hours (Plotly)
- 🗂️ **Topic Breakdown** — horizontal bar chart of most-covered topics, colour-coded by average sentiment
- 🌍 **By Country** — sentiment comparison across US, UK, India, Australia, Canada
- 🍩 **Sentiment Mix** — donut chart showing the positive/negative/neutral split of all loaded articles
- ☁️ **Keyword Cloud** — word cloud of top extracted keywords across all articles
- 📰 **Live Feed** — sortable article cards with sentiment badge, topic tag, score, and direct source link
- ⏱️ **Auto-scheduler** — background script re-runs ingestion every 30 minutes with no manual input


##  Tech Stack

| Tool | Role |
|---|---|
| **Python** | Core language — ingestion, NLP, scheduling |
| **NewsAPI** | REST API source for live global news articles |
| **pandas** | Data cleaning, deduplication, and transformation |
| **VADER / TextBlob** | Sentiment scoring and keyword extraction |
| **MySQL** | Relational storage for articles, sentiment, and trends |
| **mysql-connector-python** | Python ↔ MySQL bridge |
| **Streamlit** | Interactive web dashboard with sidebar filters |
| **Plotly** | Sentiment timeline, topic bars, country bars, donut chart |
| **WordCloud + Matplotlib** | Keyword cloud visualisation |
| **APScheduler** | Automated 30-minute ingestion loop |
| **python-dotenv** | Secure loading of API keys and DB credentials |



##  Project Structure
```
news_pulse/
├── scripts/
│   ├── db_setup.py         ← Run once to create database and tables
│   ├── db_connection.py    ← Shared MySQL connection helper
│   ├── nlp_analysis.py     ← Sentiment + keyword + topic analysis
│   ├── ingest.py           ← Fetches news and stores in MySQL
│   └── scheduler.py        ← Auto-runs ingestion every 30 minutes
├── dashboard/
│   └── app.py              ← Streamlit dashboard
├── requirements.txt
└── .env                    ← API key + DB credentials

## Future Plans

- 🌐 Support for more countries and non-English languages
- 📧 Email / Slack alerts when sentiment spikes on a specific topic
- 📤 Export filtered articles to CSV or PDF
