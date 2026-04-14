"""
scheduler.py
------------

Command: python scripts/scheduler.py
to keep feeding live data

Press Ctrl+C to stop.
"""

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
import sys
import os

sys.path.append(os.path.dirname(__file__))
from ingest import run_pipeline

scheduler = BlockingScheduler()

scheduler.add_job(
    func=run_pipeline,
    trigger=IntervalTrigger(minutes=30),
    id="news_ingestion",
    name="Fetch and store news every 30 minutes",
    replace_existing=True
)

if __name__ == "__main__":
    print(" Scheduler started. Fetching news every 30 minutes.")
    print("   Running first fetch now.")
    print("   Press Ctrl+C to stop.\n")

    # Run immediately on start
    run_pipeline()

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\n🛑 Scheduler stopped.")
