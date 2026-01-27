#!/usr/bin/env python3
"""
PULSE Signal Processor - Intelligence Layer Entry Point
========================================================
Run this script to process unprocessed signals from the raw_signals table.

Usage:
    # Process 30 signals (default)
    python process_signals.py

    # Process custom batch size
    python process_signals.py --batch-size 50

    # Dry run (no database writes)
    python process_signals.py --dry-run

    # Dry run with small batch for testing
    python process_signals.py --batch-size 5 --dry-run

Requirements:
    - .env file with API keys (OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY)
    - Supabase connection configured (SUPABASE_URL, SUPABASE_KEY)
    - At least one unprocessed signal in raw_signals table

Output:
    - Updates raw_signals: extracted_entities, sentiment_score, processed=TRUE
    - Inserts synthesized insights into insights table
    - Prints processing statistics
"""

import asyncio
import argparse
import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from dotenv import load_dotenv
from signal_processor import SignalProcessor

# Load environment variables
load_dotenv()


async def main():
    """Main entry point for signal processing."""

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='PULSE Intelligence Layer - Process Reddit signals into market insights'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=None,
        help='Number of signals to process (default: 30 or from env SIGNAL_PROCESSOR_BATCH_SIZE)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run without saving to database (for testing)'
    )

    args = parser.parse_args()

    # Print header
    print("\n" + "=" * 70)
    print("PULSE INTELLIGENCE LAYER - SIGNAL PROCESSOR")
    print("=" * 70)
    print(f"Mode: {'DRY RUN (no database writes)' if args.dry_run else 'LIVE (database writes enabled)'}")
    if args.batch_size:
        print(f"Batch size: {args.batch_size}")
    print("=" * 70 + "\n")

    try:
        # Initialize processor
        processor = SignalProcessor()

        # Run processing pipeline
        result = await processor.run(
            batch_size=args.batch_size,
            dry_run=args.dry_run
        )

        # Print results
        print("\n" + "=" * 70)
        print("RESULTS")
        print("=" * 70)
        print(f"✅ Processed {result['processed_count']} signals")
        print(f"✅ Generated {result['insights_count']} insights")
        print(f"✅ Extracted {result['tickers_count']} unique tickers")

        if args.dry_run:
            print("\n⚠️  DRY RUN: No changes were saved to the database")
            print("\nTo process signals for real, run without --dry-run flag:")
            print("  python process_signals.py")
        else:
            print("\n✅ All changes saved to database")

        print("=" * 70 + "\n")

        return 0

    except ValueError as e:
        print(f"\n❌ Configuration Error: {str(e)}")
        print("\nMake sure your .env file contains:")
        print("  - OPENAI_API_KEY")
        print("  - ANTHROPIC_API_KEY")
        print("  - GOOGLE_API_KEY")
        print("  - SUPABASE_URL")
        print("  - SUPABASE_KEY")
        return 1

    except Exception as e:
        print(f"\n❌ Processing Failed: {str(e)}")
        print("\nCheck the logs above for details.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
