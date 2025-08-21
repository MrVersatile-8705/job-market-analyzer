#!/usr/bin/env python3
"""
Debug script to test individual scraper functionality
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from loguru import logger
from src.data_collection.scrapers.builtin_scraper import BuiltinScraper

# Configure logging
logger.remove()
logger.add(sys.stdout, level="DEBUG")

def debug_builtin():
    """Debug Builtin scraper specifically."""
    
    logger.info("🧪 Debugging Builtin Scraper")
    logger.info("=" * 50)
    
    try:
        # Test with very common keywords
        scraper = BuiltinScraper()
        logger.info("✅ Builtin scraper initialized")
        
        # Test search with simple keywords
        keywords = ["Software Engineer"]  # Very common job title
        location = ""  # Empty location for broader search
        limit = 3
        
        logger.info(f"Searching for: {keywords}")
        logger.info(f"Location: '{location}' (empty for broader search)")
        logger.info(f"Limit: {limit}")
        
        job_urls = scraper.search_jobs(keywords=keywords, location=location, limit=limit)
        
        logger.info(f"Found {len(job_urls)} job URLs:")
        for i, url in enumerate(job_urls, 1):
            logger.info(f"  {i}. {url}")
            
        if job_urls:
            # Test scraping details from first job
            logger.info(f"\n🔍 Testing job details scraping...")
            first_job_url = job_urls[0]
            job_details = scraper.scrape_job_details(first_job_url)
            
            if job_details:
                logger.info(f"✅ Successfully scraped job details:")
                logger.info(f"  Title: {job_details.title}")
                logger.info(f"  Company: {job_details.company}")
                logger.info(f"  Location: {job_details.location}")
                logger.info(f"  Description length: {len(job_details.description) if job_details.description else 0} characters")
            else:
                logger.warning("❌ Failed to scrape job details")
        else:
            logger.warning("No job URLs found to test detail scraping")
            
    except Exception as e:
        logger.error(f"Error during debug: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_builtin()
