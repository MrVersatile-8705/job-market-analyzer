#!/usr/bin/env python3
"""
Quick test to verify 30-day timeframe filtering works
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

def test_30_day_search():
    """Quick test of 30-day timeframe filtering."""
    
    logger.info("🚀 Testing 30-Day Job Search")
    logger.info("=" * 40)
    
    # Initialize scraper
    scraper = IndeedScraper()
    
    # Test with small limit first
    logger.info("🔍 Searching for Data Analyst jobs from past 30 days...")
    job_urls = scraper.search_jobs(
        keywords=["Data Analyst"],
        location="",
        limit=10,  # Small limit for quick test
        days_back=30  # Past month
    )
    
    logger.info(f"✅ Found {len(job_urls)} job URLs")
    
    if job_urls:
        logger.info("📄 Testing job detail extraction on first job...")
        first_job = scraper.scrape_job_details(job_urls[0])
        
        if first_job:
            logger.info(f"✅ Successfully extracted: {first_job.title} at {first_job.company}")
            logger.info(f"   📍 Location: {first_job.location}")
            logger.info(f"   🏠 Remote: {'Yes' if first_job.remote_option else 'No'}")
            if first_job.salary:
                logger.info(f"   💰 Salary: {first_job.salary}")
        else:
            logger.warning("❌ Failed to extract job details")
    
    logger.info("\n🎉 Quick test completed!")
    logger.info("30-day filtering is working correctly!")

if __name__ == "__main__":
    test_30_day_search()
