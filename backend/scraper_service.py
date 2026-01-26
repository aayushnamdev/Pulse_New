"""
PULSE Reddit Scraper Service
============================
Scrapes r/wallstreetbets for high-quality signals using Reddit's .json endpoint.

This script:
1. Fetches hot posts from r/wallstreetbets
2. Filters for quality (upvote ratio > 0.70, upvotes > 50)
3. Calculates velocity (upvotes per hour)
4. Flags posts containing supply chain keywords
5. Returns structured data ready for database insertion
6. Saves to Supabase in production mode
"""

import requests
import time
import os
from datetime import datetime
from typing import List, Dict, Optional
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database service (will fail gracefully if not available)
try:
    from database_service import DatabaseService
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    print("⚠️  database_service not available - running in test mode only")


class RedditScraper:
    """
    Scrapes Reddit using the .json URL trick (no API key needed).
    """

    def __init__(
        self,
        subreddit: Optional[str] = None,
        min_upvote_ratio: Optional[float] = None,
        min_upvotes: Optional[int] = None,
        fetch_limit: Optional[int] = None
    ):
        """
        Initialize the scraper.

        Args:
            subreddit: The subreddit to scrape (defaults to env var or 'wallstreetbets')
            min_upvote_ratio: Minimum upvote ratio filter (defaults to env var or 0.70)
            min_upvotes: Minimum upvotes filter (defaults to env var or 50)
            fetch_limit: Number of posts to fetch (defaults to env var or 100)
        """
        # Load configuration from environment or use defaults
        self.subreddit = subreddit or os.getenv("REDDIT_SUBREDDIT", "wallstreetbets")
        self.min_upvote_ratio = min_upvote_ratio or float(os.getenv("MIN_UPVOTE_RATIO", "0.70"))
        self.min_upvotes = min_upvotes or int(os.getenv("MIN_UPVOTES", "50"))
        self.fetch_limit = fetch_limit or int(os.getenv("REDDIT_FETCH_LIMIT", "100"))

        self.base_url = f"https://www.reddit.com/r/{self.subreddit}/hot.json"

        # Quality keywords that indicate supply chain signals
        self.quality_keywords = ["delay", "inventory", "backorder", "shortage"]

        # Reddit requires a user agent to avoid 429 errors
        self.headers = {
            "User-Agent": "PULSE/1.0 (Educational Project)"
        }

    def fetch_hot_posts(self, limit: int = 100) -> List[Dict]:
        """
        Fetch hot posts from the subreddit.

        Args:
            limit: Number of posts to fetch (default: 100)

        Returns:
            List of post dictionaries with processed data
        """
        print(f"🔍 Fetching hot posts from r/{self.subreddit}...")

        try:
            # Make request to Reddit's .json endpoint
            params = {"limit": limit}
            response = requests.get(
                self.base_url,
                headers=self.headers,
                params=params,
                timeout=10
            )

            # Check if request was successful
            if response.status_code != 200:
                print(f"❌ Error: Received status code {response.status_code}")
                return []

            # Parse JSON response
            data = response.json()
            posts = data.get("data", {}).get("children", [])

            print(f"✅ Fetched {len(posts)} posts")

            # Process each post
            processed_posts = []
            for post in posts:
                post_data = post.get("data", {})
                processed = self._process_post(post_data)

                # Only keep posts that pass our filters
                if processed and self._passes_filter(processed):
                    processed_posts.append(processed)

            print(f"✅ {len(processed_posts)} posts passed quality filters")
            return processed_posts

        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            return []

    def _process_post(self, post_data: Dict) -> Dict:
        """
        Extract and process relevant fields from a Reddit post.

        Args:
            post_data: Raw post data from Reddit API

        Returns:
            Processed post dictionary with calculated fields
        """
        try:
            # Extract core fields
            post_id = post_data.get("id")
            title = post_data.get("title", "")
            selftext = post_data.get("selftext", "")
            ups = post_data.get("ups", 0)
            num_comments = post_data.get("num_comments", 0)
            upvote_ratio = post_data.get("upvote_ratio", 0.0)
            created_utc = post_data.get("created_utc", 0)
            author = post_data.get("author", "[deleted]")

            # Calculate post age in hours
            current_time = time.time()
            age_seconds = current_time - created_utc
            age_hours = age_seconds / 3600

            # Calculate velocity (upvotes per hour)
            # Avoid division by zero for very new posts
            velocity = ups / max(age_hours, 0.1)

            # Check if post contains quality keywords
            content = f"{title} {selftext}".lower()
            is_quality_signal = any(
                keyword in content for keyword in self.quality_keywords
            )

            # Convert Unix timestamp to readable datetime
            created_at = datetime.fromtimestamp(created_utc).isoformat()

            return {
                "source": "reddit",
                "source_id": post_id,
                "subreddit": self.subreddit,
                "title": title,
                "content": selftext,
                "author": author,
                "upvotes": ups,
                "num_comments": num_comments,
                "upvote_ratio": upvote_ratio,
                "velocity": round(velocity, 2),
                "is_quality_signal": is_quality_signal,
                "age_hours": round(age_hours, 2),
                "created_at": created_at,
                "scraped_at": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"⚠️  Error processing post: {e}")
            return None

    def _passes_filter(self, post: Dict) -> bool:
        """
        Check if a post meets our quality thresholds.

        Filter criteria:
        - Upvote ratio > configured threshold (default: 0.70)
        - Upvotes > configured threshold (default: 50)

        Args:
            post: Processed post dictionary

        Returns:
            True if post passes filters, False otherwise
        """
        return (
            post.get("upvote_ratio", 0) > self.min_upvote_ratio and
            post.get("upvotes", 0) > self.min_upvotes
        )

    def print_results(self, posts: List[Dict]):
        """
        Pretty-print results to terminal for testing.

        Args:
            posts: List of processed posts
        """
        print("\n" + "="*80)
        print(f"📊 PULSE SCRAPER RESULTS - r/{self.subreddit}")
        print("="*80 + "\n")

        if not posts:
            print("❌ No posts matched the filters.\n")
            return

        for idx, post in enumerate(posts, 1):
            print(f"Post #{idx}")
            print(f"  ID: {post['source_id']}")
            print(f"  Title: {post['title'][:60]}...")
            print(f"  Upvotes: {post['upvotes']} | Comments: {post['num_comments']}")
            print(f"  Upvote Ratio: {post['upvote_ratio']:.2f}")
            print(f"  Velocity: {post['velocity']:.2f} upvotes/hour")
            print(f"  Age: {post['age_hours']:.1f} hours")
            print(f"  Quality Signal: {'🟢 YES' if post['is_quality_signal'] else '⚪ NO'}")
            print(f"  Author: u/{post['author']}")
            print()

        # Summary statistics
        total_posts = len(posts)
        quality_signals = sum(1 for p in posts if p['is_quality_signal'])
        avg_velocity = sum(p['velocity'] for p in posts) / total_posts

        print("="*80)
        print("📈 SUMMARY")
        print("="*80)
        print(f"  Total Posts: {total_posts}")
        print(f"  Quality Signals: {quality_signals} ({quality_signals/total_posts*100:.1f}%)")
        print(f"  Avg Velocity: {avg_velocity:.2f} upvotes/hour")
        print("="*80 + "\n")

    def run(self, save_to_db: bool = True, print_output: bool = True) -> Dict:
        """
        Main execution method: scrape Reddit and optionally save to database.

        This is the primary method to use in production (Railway cron job).

        Args:
            save_to_db: If True, save results to Supabase (default: True)
            print_output: If True, print results to console (default: True)

        Returns:
            Dictionary with execution summary
        """
        print("\n" + "="*80)
        print("🚀 PULSE SCRAPER - PRODUCTION RUN")
        print("="*80)
        print(f"  Subreddit: r/{self.subreddit}")
        print(f"  Fetch Limit: {self.fetch_limit}")
        print(f"  Min Upvote Ratio: {self.min_upvote_ratio}")
        print(f"  Min Upvotes: {self.min_upvotes}")
        print(f"  Save to DB: {save_to_db}")
        print("="*80 + "\n")

        # Step 1: Scrape Reddit
        posts = self.fetch_hot_posts(limit=self.fetch_limit)

        # Step 2: Print results if requested
        if print_output and posts:
            self.print_results(posts)

        # Step 3: Save to database if requested
        db_result = None
        if save_to_db and posts:
            if not DB_AVAILABLE:
                print("❌ Cannot save to database: database_service not available")
                return {
                    "success": False,
                    "scraped": len(posts),
                    "saved": 0,
                    "error": "Database service not available"
                }

            try:
                print("💾 Saving to Supabase...")
                db = DatabaseService()
                db_records = db.transform_to_db_format(posts)
                db_result = db.batch_insert(db_records)

                if db_result["success"]:
                    print(f"✅ Saved {db_result['inserted']} signals to database")
                else:
                    print(f"❌ Database save failed: {db_result.get('error')}")

            except Exception as e:
                print(f"❌ Database error: {e}")
                db_result = {"success": False, "error": str(e)}

        # Step 4: Return summary
        return {
            "success": True,
            "scraped": len(posts),
            "quality_signals": sum(1 for p in posts if p['is_quality_signal']),
            "saved_to_db": db_result["inserted"] if db_result and db_result.get("success") else 0,
            "db_success": db_result["success"] if db_result else False,
            "timestamp": datetime.now().isoformat()
        }


# ============================================================================
# TEST BLOCK - Run this file directly to test the scraper
# ============================================================================

if __name__ == "__main__":
    # Check if we're in production mode (via environment variable)
    environment = os.getenv("ENVIRONMENT", "development")
    is_production = environment == "production"

    if is_production:
        # PRODUCTION MODE - Used by Railway cron job
        print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║              PULSE REDDIT SCRAPER - PRODUCTION            ║
    ╚═══════════════════════════════════════════════════════════╝
        """)

        # Initialize scraper with environment configuration
        scraper = RedditScraper()

        # Run full pipeline (scrape + save to DB)
        result = scraper.run(save_to_db=True, print_output=False)

        # Log results
        print("\n" + "="*80)
        print("📊 EXECUTION SUMMARY")
        print("="*80)
        print(f"  Scraped: {result['scraped']} posts")
        print(f"  Quality Signals: {result['quality_signals']}")
        print(f"  Saved to DB: {result['saved_to_db']}")
        print(f"  DB Success: {result['db_success']}")
        print(f"  Timestamp: {result['timestamp']}")
        print("="*80)

    else:
        # DEVELOPMENT MODE - Local testing without database
        print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                  PULSE REDDIT SCRAPER                     ║
    ║                    LOCAL TEST MODE                        ║
    ╚═══════════════════════════════════════════════════════════╝
        """)

        # Initialize scraper
        scraper = RedditScraper(subreddit="wallstreetbets")

        # Fetch and process posts (test mode - smaller limit)
        posts = scraper.fetch_hot_posts(limit=50)

        # Display results
        scraper.print_results(posts)

        # Save results to JSON file for inspection
        if posts:
            output_file = "test_scraper_output.json"
            with open(output_file, "w") as f:
                json.dump(posts, f, indent=2)
            print(f"💾 Results saved to {output_file}")

        # Offer to test database connection
        if DB_AVAILABLE:
            print("\n💡 Database service is available!")
            print("   To test database insertion, run: scraper.run(save_to_db=True)")
        else:
            print("\n💡 To test with database:")
            print("   1. Fill in your .env file with Supabase credentials")
            print("   2. Run: python database_service.py (to test connection)")
            print("   3. Run this script again")
