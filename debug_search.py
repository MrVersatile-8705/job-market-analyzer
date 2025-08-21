#!/usr/bin/env python3
"""
Debug test to check search parameters and page response
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from loguru import logger
from src.data_collection.scrapers.indeed_scraper import IndeedScraper

# Configure simple logging
logger.remove()
logger.add(sys.stdout, level="INFO")

def debug_search():
    """Debug the search functionality."""
    
    logger.info("🔍 Debug Search Test")
    logger.info("=" * 30)
    
    # Test different time ranges
    scraper = IndeedScraper()
    
    test_cases = [
        {"days_back": 1, "name": "Past 1 day"},
        {"days_back": 7, "name": "Past 7 days"},
        {"days_back": 14, "name": "Past 14 days"},
        {"days_back": 30, "name": "Past 30 days"},
        {"days_back": None, "name": "No time filter"}  # Test without time filter
    ]
    
    for test_case in test_cases:
        logger.info(f"\n📊 Testing: {test_case['name']}")
        
        try:
            if test_case['days_back'] is None:
                # Test original method without days_back
                job_urls = scraper.search_jobs(
                    keywords=["Data Analyst"],
                    location="",
                    limit=5
                )
            else:
                job_urls = scraper.search_jobs(
                    keywords=["Data Analyst"],
                    location="",
                    limit=5,
                    days_back=test_case['days_back']
                )
            
            logger.info(f"   ✅ Found {len(job_urls)} jobs")
            
            if job_urls:
                break  # Stop at first successful search
                
        except Exception as e:
            logger.error(f"   ❌ Error: {e}")
    
    logger.info("\n🎉 Debug test completed!")

if __name__ == "__main__":
    debug_search()
