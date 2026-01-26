#!/usr/bin/env python3
"""
Quick test script to verify the full pipeline works
"""

from scraper_service import RedditScraper

print("\n" + "="*80)
print("🧪 TESTING FULL PIPELINE: Reddit → Supabase")
print("="*80 + "\n")

# Initialize scraper
scraper = RedditScraper()

# Run full pipeline
result = scraper.run(save_to_db=True, print_output=False)

# Show results
print("\n" + "="*80)
print("📊 PIPELINE TEST RESULTS")
print("="*80)
print(f"  ✅ Scraped Posts: {result['scraped']}")
print(f"  🟢 Quality Signals: {result['quality_signals']}")
print(f"  💾 Saved to DB: {result['saved_to_db']}")
print(f"  🔗 DB Success: {result['db_success']}")
print("="*80 + "\n")

if result['db_success']:
    print("✅ FULL PIPELINE TEST PASSED!")
    print("   Go check your Supabase dashboard - you should see data in raw_signals!")
else:
    print("❌ Database save failed - check errors above")
