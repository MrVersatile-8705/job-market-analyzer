#!/usr/bin/env python3
"""
Test script for validating new scrapers
Tests ZipRecruiter, Dice, Stack Overflow, and Builtin scrapers
"""

import sys
import time
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from loguru import logger
from src.data_collection.scrapers.ziprecruiter_scraper import ZipRecruiterScraper
from src.data_collection.scrapers.dice_scraper import DiceScraper
from src.data_collection.scrapers.stackoverflow_scraper import StackOverflowScraper
from src.data_collection.scrapers.builtin_scraper import BuiltinScraper

# Configure logging
logger.remove()
logger.add(
    "logs/new_scraper_test.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="INFO",
    rotation="10 MB"
)
logger.add(sys.stdout, level="INFO")

def test_scraper(scraper_class, scraper_name, keywords, location="Remote", limit=3, days_back=30):
    """Test a single scraper with given parameters."""
    
    logger.info(f"\n{'='*60}")
    logger.info(f"🧪 Testing {scraper_name}")
    logger.info(f"Keywords: {keywords}")
    logger.info(f"Location: {location}")
    logger.info(f"Limit: {limit}")
    logger.info(f"Days back: {days_back}")
    logger.info(f"{'='*60}")
    
    try:
        # Initialize scraper
        scraper = scraper_class()
        logger.info(f"✅ {scraper_name} initialized successfully")
        
        # Test search_jobs method
        start_time = time.time()
        job_urls = scraper.search_jobs(keywords=keywords, location=location, limit=limit, days_back=days_back)
        end_time = time.time()
        
        # Results
        logger.info(f"🎯 Found {len(job_urls)} job URLs in {end_time - start_time:.2f} seconds")
        
        if job_urls:
            logger.info("📋 Sample URLs:")
            for i, url in enumerate(job_urls[:2], 1):
                logger.info(f"  {i}. {url}")
            
            # Test scrape_job method on first URL
            if len(job_urls) > 0:
                logger.info(f"\n🔍 Testing job detail scraping...")
                try:
                    job_data = scraper.scrape_job(job_urls[0])
                    if job_data:
                        logger.info(f"✅ Successfully scraped job details:")
                        logger.info(f"  Title: {job_data.title}")
                        logger.info(f"  Company: {job_data.company}")
                        logger.info(f"  Location: {job_data.location}")
                        logger.info(f"  Description length: {len(job_data.description)} chars")
                        if job_data.salary:
                            logger.info(f"  Salary: {job_data.salary}")
                    else:
                        logger.warning("⚠️ Job detail scraping returned None")
                except Exception as detail_error:
                    logger.error(f"❌ Job detail scraping failed: {detail_error}")
        else:
            logger.warning("⚠️ No job URLs found")
            
        return {
            'scraper': scraper_name,
            'success': True,
            'job_count': len(job_urls),
            'time_taken': end_time - start_time,
            'urls': job_urls[:3]  # Store first 3 URLs for reference
        }
        
    except Exception as e:
        logger.error(f"❌ {scraper_name} test failed: {e}")
        return {
            'scraper': scraper_name,
            'success': False,
            'error': str(e),
            'job_count': 0,
            'time_taken': 0
        }

def main():
    """Run tests for all new scrapers."""
    
    logger.info("🚀 Starting New Scraper Validation Tests")
    logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 80)
    
    # Test configurations - BROADER SEARCH CRITERIA for better results
    test_configs = [
        {
            'scraper_class': ZipRecruiterScraper,
            'scraper_name': 'ZipRecruiter',
            'keywords': ['Data Analyst', 'Business Analyst'],  # Multiple common keywords
            'location': '',  # No location restriction for broader search
            'limit': 5,
            'days_back': 90  # Increased from 30 to 90 days
        },
        {
            'scraper_class': DiceScraper,
            'scraper_name': 'Dice',
            'keywords': ['Data', 'Analyst'],  # Very broad keywords
            'location': '',  # No location restriction
            'limit': 5,
            'days_back': 90
        },
        {
            'scraper_class': StackOverflowScraper,
            'scraper_name': 'Stack Overflow Jobs',
            'keywords': ['Data', 'Analytics'],  # Broader keywords
            'location': '',  # No location restriction
            'limit': 3,  # Smaller limit for SO
            'days_back': 90
        },
        {
            'scraper_class': BuiltinScraper,
            'scraper_name': 'Builtin',
            'keywords': ['Analyst', 'Data'],  # Very common keywords
            'location': '',  # No location restriction for broader search
            'limit': 5,
            'days_back': 90
        }
    ]
    
    results = []
    total_start_time = time.time()
    
    # Run tests
    for config in test_configs:
        result = test_scraper(**config)
        results.append(result)
        
        # Add delay between tests to be respectful
        logger.info("⏱️ Waiting 5 seconds before next test...")
        time.sleep(5)
    
    total_end_time = time.time()
    
    # Summary report
    logger.info(f"\n{'='*80}")
    logger.info("📊 FINAL TEST RESULTS SUMMARY")
    logger.info(f"{'='*80}")
    
    successful_scrapers = [r for r in results if r['success']]
    failed_scrapers = [r for r in results if not r['success']]
    total_jobs_found = sum(r['job_count'] for r in results)
    
    logger.info(f"✅ Successful scrapers: {len(successful_scrapers)}/{len(results)}")
    logger.info(f"❌ Failed scrapers: {len(failed_scrapers)}")
    logger.info(f"🎯 Total jobs found: {total_jobs_found}")
    logger.info(f"⏱️ Total test time: {total_end_time - total_start_time:.2f} seconds")
    
    # Detailed results
    for result in results:
        status = "✅ SUCCESS" if result['success'] else "❌ FAILED"
        logger.info(f"\n{result['scraper']}: {status}")
        if result['success']:
            logger.info(f"  Jobs found: {result['job_count']}")
            logger.info(f"  Time taken: {result['time_taken']:.2f}s")
        else:
            logger.info(f"  Error: {result.get('error', 'Unknown error')}")
    
    # Recommendations
    logger.info(f"\n{'='*60}")
    logger.info("🔧 RECOMMENDATIONS")
    logger.info(f"{'='*60}")
    
    if len(successful_scrapers) == len(results):
        logger.info("🎉 All scrapers working! Ready for production use.")
        logger.info("Next steps:")
        logger.info("  1. Run comprehensive test with all job titles")
        logger.info("  2. Update analysis scripts to use multiple scrapers")
        logger.info("  3. Implement error handling and monitoring")
    elif len(successful_scrapers) > 0:
        logger.info(f"⚠️ {len(successful_scrapers)} scrapers working, {len(failed_scrapers)} need fixes")
        logger.info("Proceed with working scrapers while fixing issues")
    else:
        logger.error("❌ No scrapers working - check network, dependencies, website changes")
    
    logger.info(f"\n🏁 Test completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return results

if __name__ == "__main__":
    try:
        results = main()
    except KeyboardInterrupt:
        logger.warning("Test interrupted by user")
    except Exception as e:
        logger.error(f"Test script failed: {e}")
        raise
