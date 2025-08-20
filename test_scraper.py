"""
Test script for the Indeed scraper
"""
import sys
import os
from pathlib import Path

# Add the src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import our modules
from config.logging_config import logger
from config.settings import settings
from data_collection.scrapers.indeed_scraper import IndeedScraper

def test_indeed_scraper():
    """Test the Indeed scraper with a small sample."""
    logger.info("Starting Indeed scraper test")
    
    # Test keywords for data analyst positions
    keywords = ["data analyst", "business analyst","business intelligence analyst", 
                "senior data analyst","senior business analyst", "senior business intelligence analyst"]
    location = "Remote"
    limit = 3  # Small limit for testing
    
    try:
        with IndeedScraper() as scraper:
            logger.info("Testing job search...")
            job_urls = scraper.search_jobs(keywords, location, limit)
            logger.info(f"Found {len(job_urls)} job URLs")
            
            if job_urls:
                logger.info("Testing job details scraping...")
                # Test scraping the first job
                job = scraper.scrape_job_details(job_urls[0])
                
                if job:
                    logger.info(f"Successfully scraped job:")
                    logger.info(f"  Title: {job.title}")
                    logger.info(f"  Company: {job.company}")
                    logger.info(f"  Location: {job.location}")
                    logger.info(f"  Salary: {job.salary}")
                    logger.info(f"  Remote: {job.remote_option}")
                    logger.info(f"  URL: {job.url}")
                    logger.info(f"  Description (first 500 chars): {job.description[:500]}...")
                else:
                    logger.warning("Failed to scrape job details")
            else:
                logger.warning("No job URLs found")
                
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise

if __name__ == "__main__":
    test_indeed_scraper()
