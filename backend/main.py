#!/usr/bin/env python3
"""
PULSE Main Entry Point
======================
This is the main script that Railway will execute via cron job.

Cron Schedule: 0 */6 * * *  (Every 6 hours)
"""

from scraper_service import RedditScraper
from datetime import datetime


def main():
    """
    Main execution function for Railway cron job.
    """
    print(f"\n{'='*80}")
    print(f"🚀 PULSE SCRAPER CRON JOB - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")

    try:
        # Initialize scraper (reads from .env)
        scraper = RedditScraper()

        # Run full pipeline: scrape + save to Supabase
        result = scraper.run(save_to_db=True, print_output=False)

        # Log execution summary
        print(f"\n{'='*80}")
        print("✅ CRON JOB COMPLETED SUCCESSFULLY")
        print(f"{'='*80}")
        print(f"  Scraped: {result['scraped']} posts")
        print(f"  Quality Signals: {result['quality_signals']}")
        print(f"  Saved to Database: {result['saved_to_db']}")
        print(f"  Timestamp: {result['timestamp']}")
        print(f"{'='*80}\n")

        return 0  # Success

    except Exception as e:
        print(f"\n{'='*80}")
        print("❌ CRON JOB FAILED")
        print(f"{'='*80}")
        print(f"  Error: {e}")
        print(f"  Timestamp: {datetime.now().isoformat()}")
        print(f"{'='*80}\n")

        return 1  # Failure


if __name__ == "__main__":
    exit(main())
