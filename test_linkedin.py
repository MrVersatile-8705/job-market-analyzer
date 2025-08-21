#!/usr/bin/env python3
"""
LinkedIn Scraper Test

Quick test to verify LinkedIn scraper functionality.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from loguru import logger
from src.data_collection.scrapers.linkedin_scraper import LinkedInScraper

# Configure logging
logger.remove()
logger.add(sys.stdout, level="INFO")

def test_linkedin_scraper():
    """Test LinkedIn scraper functionality."""
    
    logger.info("🔍 Testing LinkedIn Scraper")
    logger.info("=" * 40)
    
    try:
        # Initialize scraper
        scraper = LinkedInScraper()
        
        # Test search (small limit for testing)
        keywords = ["Data Analyst"]
        location = "Remote"
        limit = 3
        
        logger.info(f"Searching for: {keywords}")
        logger.info(f"Location: {location}")
        logger.info(f"Limit: {limit}")
        
        # Search for job URLs
        job_urls = scraper.search_jobs(keywords, location, limit)
        
        logger.info(f"✅ Found {len(job_urls)} job URLs")
        
        if job_urls:
            logger.info("Sample URLs:")
            for i, url in enumerate(job_urls[:3], 1):
                logger.info(f"  {i}. {url}")
            
            # Test job detail scraping for first URL
            logger.info("\n📄 Testing job detail scraping...")
            first_job = scraper.scrape_job_details(job_urls[0])
            
            if first_job:
                logger.info("✅ Job detail scraping successful!")
                logger.info(f"Title: {first_job.title}")
                logger.info(f"Company: {first_job.company}")
                logger.info(f"Location: {first_job.location}")
                logger.info(f"Remote: {first_job.remote_option}")
            else:
                logger.warning("❌ Job detail scraping failed")
        else:
            logger.warning("No job URLs found - LinkedIn may be blocking requests")
            
    except Exception as e:
        logger.error(f"❌ LinkedIn scraper test failed: {e}")
        return False
    
    logger.info("\n✅ LinkedIn scraper test completed")
    return True

if __name__ == "__main__":
    test_linkedin_scraper()
