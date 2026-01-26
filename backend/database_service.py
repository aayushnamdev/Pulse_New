"""
PULSE Database Service
=====================
Handles all Supabase database operations for storing scraped signals.

This service:
1. Connects to Supabase using credentials from .env
2. Transforms scraped data into database-ready format
3. Performs batch insertion into raw_signals table
4. Handles duplicate detection and error logging
"""

import os
from typing import List, Dict, Optional
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class DatabaseService:
    """
    Manages database operations for PULSE.
    """

    def __init__(self):
        """
        Initialize the Supabase client using environment variables.
        """
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")

        # Validate credentials exist
        if not self.supabase_url or not self.supabase_key:
            raise ValueError(
                "❌ Missing Supabase credentials! "
                "Please set SUPABASE_URL and SUPABASE_KEY in your .env file"
            )

        # Initialize Supabase client
        try:
            self.client: Client = create_client(self.supabase_url, self.supabase_key)
            print("✅ Connected to Supabase")
        except Exception as e:
            raise ConnectionError(f"❌ Failed to connect to Supabase: {e}")

    def transform_to_db_format(self, scraped_posts: List[Dict]) -> List[Dict]:
        """
        Transform scraped Reddit posts into database-ready format.

        Args:
            scraped_posts: List of posts from RedditScraper

        Returns:
            List of dictionaries matching raw_signals table schema
        """
        db_records = []

        for post in scraped_posts:
            # Build engagement_metrics JSON
            engagement_metrics = {
                "upvotes": post.get("upvotes", 0),
                "num_comments": post.get("num_comments", 0),
                "upvote_ratio": post.get("upvote_ratio", 0.0),
                "velocity": post.get("velocity", 0.0)
            }

            # Create database record
            record = {
                "source": post.get("source", "reddit"),
                "source_id": post.get("source_id"),
                "subreddit": post.get("subreddit"),
                "title": post.get("title"),
                "content": post.get("content"),
                "author_id": post.get("author"),
                "engagement_metrics": engagement_metrics,
                "is_quality_signal": post.get("is_quality_signal", False),
                "source_created_at": post.get("created_at"),
                "scraped_at": post.get("scraped_at"),
                "age_hours": post.get("age_hours"),
                "processed": False  # Will be processed by Claude later
            }

            db_records.append(record)

        return db_records

    def batch_insert(self, records: List[Dict]) -> Dict[str, any]:
        """
        Insert multiple records into raw_signals table.

        Uses Supabase's upsert to handle duplicates gracefully.

        Args:
            records: List of database-ready records

        Returns:
            Dictionary with success status and stats
        """
        if not records:
            return {
                "success": True,
                "inserted": 0,
                "skipped": 0,
                "message": "No records to insert"
            }

        try:
            print(f"💾 Inserting {len(records)} records into Supabase...")

            # Use upsert to handle duplicates (based on source_id uniqueness)
            # on_conflict='source_id' will skip duplicates instead of erroring
            response = self.client.table('raw_signals').upsert(
                records,
                on_conflict='source_id',
                returning='minimal'  # Faster, we don't need returned data
            ).execute()

            print(f"✅ Successfully inserted {len(records)} records")

            return {
                "success": True,
                "inserted": len(records),
                "skipped": 0,
                "message": f"Inserted {len(records)} records"
            }

        except Exception as e:
            print(f"❌ Database insertion error: {e}")
            return {
                "success": False,
                "inserted": 0,
                "skipped": 0,
                "error": str(e)
            }

    def check_duplicate(self, source_id: str) -> bool:
        """
        Check if a signal already exists in the database.

        Args:
            source_id: The source_id to check

        Returns:
            True if exists, False otherwise
        """
        try:
            response = self.client.table('raw_signals').select('id').eq(
                'source_id', source_id
            ).execute()

            return len(response.data) > 0

        except Exception as e:
            print(f"⚠️  Error checking duplicate: {e}")
            return False

    def get_recent_signals(self, limit: int = 10, quality_only: bool = False) -> List[Dict]:
        """
        Retrieve recent signals from the database (for testing/verification).

        Args:
            limit: Number of records to retrieve
            quality_only: If True, only return quality signals

        Returns:
            List of signal records
        """
        try:
            query = self.client.table('raw_signals').select('*')

            if quality_only:
                query = query.eq('is_quality_signal', True)

            response = query.order('source_created_at', desc=True).limit(limit).execute()

            return response.data

        except Exception as e:
            print(f"❌ Error retrieving signals: {e}")
            return []

    def get_stats(self) -> Dict[str, any]:
        """
        Get database statistics (total signals, quality signals, etc.).

        Returns:
            Dictionary with database stats
        """
        try:
            # Total signals
            total_response = self.client.table('raw_signals').select(
                'id', count='exact'
            ).execute()
            total_count = total_response.count

            # Quality signals
            quality_response = self.client.table('raw_signals').select(
                'id', count='exact'
            ).eq('is_quality_signal', True).execute()
            quality_count = quality_response.count

            # Unprocessed signals
            unprocessed_response = self.client.table('raw_signals').select(
                'id', count='exact'
            ).eq('processed', False).execute()
            unprocessed_count = unprocessed_response.count

            return {
                "total_signals": total_count,
                "quality_signals": quality_count,
                "unprocessed_signals": unprocessed_count,
                "quality_percentage": round(quality_count / total_count * 100, 1) if total_count > 0 else 0
            }

        except Exception as e:
            print(f"❌ Error getting stats: {e}")
            return {}


# ============================================================================
# TEST BLOCK - Run this file directly to test database connection
# ============================================================================

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║              PULSE DATABASE SERVICE TEST                  ║
    ╚═══════════════════════════════════════════════════════════╝
    """)

    try:
        # Initialize database service
        db = DatabaseService()

        # Get current stats
        print("\n📊 Current Database Stats:")
        stats = db.get_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")

        # Test data (sample post)
        test_post = {
            "source": "reddit",
            "source_id": f"test_{datetime.now().timestamp()}",
            "subreddit": "wallstreetbets",
            "title": "Test Post - Database Connection",
            "content": "This is a test post to verify database connectivity",
            "author": "test_user",
            "upvotes": 100,
            "num_comments": 50,
            "upvote_ratio": 0.95,
            "velocity": 10.5,
            "is_quality_signal": True,
            "age_hours": 5.0,
            "created_at": datetime.now().isoformat(),
            "scraped_at": datetime.now().isoformat()
        }

        # Transform and insert
        print("\n🧪 Testing batch insert with sample data...")
        db_records = db.transform_to_db_format([test_post])
        result = db.batch_insert(db_records)

        if result["success"]:
            print(f"✅ Test insert successful: {result['message']}")
        else:
            print(f"❌ Test insert failed: {result.get('error')}")

        # Get recent signals
        print("\n📋 Recent Signals (Last 5):")
        recent = db.get_recent_signals(limit=5)
        for idx, signal in enumerate(recent, 1):
            print(f"  {idx}. {signal.get('title', 'N/A')[:50]}... "
                  f"[{signal.get('source')}] - Quality: {signal.get('is_quality_signal')}")

        print("\n✅ Database service test completed!")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("\nMake sure you have:")
        print("  1. Created your Supabase project")
        print("  2. Run the schema.sql file in Supabase SQL Editor")
        print("  3. Filled in SUPABASE_URL and SUPABASE_KEY in .env file")
