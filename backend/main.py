#!/usr/bin/env python3
"""
PULSE Main Entry Point
======================
This is the main script that Railway will execute via cron job.

Cron Schedule: 0 */6 * * *  (Every 6 hours)

Pipeline:
1. Scrape Reddit for new signals
2. Process signals through intelligence layer (AI analysis)
"""

from scraper_service import RedditScraper
from signal_processor import SignalProcessor
from datetime import datetime
import asyncio


def main():
    """
    Main execution function for Railway cron job.
    Runs scraper + intelligence layer in sequence.
    """
    print(f"\n{'='*80}")
    print(f"🚀 PULSE CRON JOB - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")

    try:
        # ====================================================================
        # STEP 1: SCRAPE REDDIT
        # ====================================================================
        print(f"{'='*80}")
        print("📡 STEP 1: SCRAPING REDDIT")
        print(f"{'='*80}\n")

        scraper = RedditScraper()
        scrape_result = scraper.run(save_to_db=True, print_output=False)

        print(f"\n{'='*80}")
        print("✅ SCRAPING COMPLETED")
        print(f"{'='*80}")
        print(f"  Scraped: {scrape_result['scraped']} posts")
        print(f"  Quality Signals: {scrape_result['quality_signals']}")
        print(f"  Saved to Database: {scrape_result['saved_to_db']}")
        print(f"{'='*80}\n")

        # ====================================================================
        # STEP 2: PROCESS SIGNALS (INTELLIGENCE LAYER)
        # ====================================================================
        print(f"{'='*80}")
        print("🧠 STEP 2: PROCESSING SIGNALS (INTELLIGENCE LAYER)")
        print(f"{'='*80}\n")

        processor = SignalProcessor()

        # Process all unprocessed signals (up to 50 per run)
        process_result = asyncio.run(
            processor.run(batch_size=50, dry_run=False)
        )

        print(f"\n{'='*80}")
        print("✅ INTELLIGENCE PROCESSING COMPLETED")
        print(f"{'='*80}")
        print(f"  Signals Processed: {process_result['processed_count']}")
        print(f"  Insights Generated: {process_result['insights_count']}")
        print(f"  Tickers Extracted: {process_result['tickers_count']}")
        print(f"{'='*80}\n")

        # ====================================================================
        # FINAL SUMMARY
        # ====================================================================
        print(f"{'='*80}")
        print("✅ CRON JOB COMPLETED SUCCESSFULLY")
        print(f"{'='*80}")
        print(f"  Total Posts Scraped: {scrape_result['scraped']}")
        print(f"  Signals Processed: {process_result['processed_count']}")
        print(f"  Insights Generated: {process_result['insights_count']}")
        print(f"  Timestamp: {scrape_result['timestamp']}")
        print(f"{'='*80}\n")

        return 0  # Success

    except Exception as e:
        print(f"\n{'='*80}")
        print("❌ CRON JOB FAILED")
        print(f"{'='*80}")
        print(f"  Error: {e}")
        print(f"  Timestamp: {datetime.now().isoformat()}")
        print(f"{'='*80}\n")

        # Print traceback for debugging
        import traceback
        traceback.print_exc()

        return 1  # Failure


if __name__ == "__main__":
    exit(main())
