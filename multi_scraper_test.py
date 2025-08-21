#!/usr/bin/env python3
"""
Multi-Scraper Test Script
Tests all implemented job scrapers with analytics-focused job searches.
"""

import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from loguru import logger
from src.config.settings import Settings
from src.config.job_search_config import get_all_job_titles
from src.data_collection.scrapers.indeed_scraper import IndeedScraper
from src.data_collection.scrapers.ziprecruiter_scraper import ZipRecruiterScraper
from src.data_collection.scrapers.dice_scraper import DiceScraper
from src.data_collection.scrapers.stackoverflow_scraper import StackOverflowScraper
from src.data_collection.scrapers.builtin_scraper import BuiltinScraper

# Configure logging
logger.remove()
logger.add(
    "logs/multi_scraper_test.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="INFO",
    rotation="10 MB"
)
logger.add(sys.stdout, level="INFO")

def test_all_scrapers():
    """Test all available job scrapers with analytics roles."""
    
    logger.info("🚀 Multi-Scraper Analytics Job Test")
    logger.info("=" * 60)
    
    # Test configuration
    test_configs = [
        {
            "name": "Core Analytics - NYC",
            "keywords": ["Data Analyst", "Business Analyst"],
            "location": "New York, NY",
            "limit": 5
        },
        {
            "name": "Data Science - Remote",
            "keywords": ["Data Scientist", "Analytics Engineer"],
            "location": "Remote",
            "limit": 5
        },
        {
            "name": "BI Roles - San Francisco",
            "keywords": ["BI Developer", "BI Analyst"],
            "location": "San Francisco, CA",
            "limit": 5
        }
    ]
    
    # Initialize all scrapers
    scrapers = {
        "Indeed": IndeedScraper(),
        "ZipRecruiter": ZipRecruiterScraper(),
        "Dice": DiceScraper(),
        "StackOverflow": StackOverflowScraper(),
        "Builtin": BuiltinScraper()
    }
    
    logger.info(f"📊 Testing {len(scrapers)} scrapers with {len(test_configs)} configurations")
    logger.info(f"🎯 Analytics job titles: {', '.join(get_all_job_titles()[:5])}... (20 total)")
    
    all_results = []
    
    for i, config in enumerate(test_configs, 1):
        logger.info(f"\n📋 Test Configuration {i}: {config['name']}")
        logger.info(f"Keywords: {', '.join(config['keywords'])}")
        logger.info(f"Location: {config['location']}")
        logger.info(f"Limit: {config['limit']} jobs per scraper")
        logger.info("-" * 50)
        
        config_results = {
            'config': config,
            'scraper_results': {},
            'total_jobs': 0,
            'successful_scrapers': 0
        }
        
        for scraper_name, scraper in scrapers.items():
            logger.info(f"🔍 Testing {scraper_name}...")
            
            try:
                start_time = time.time()
                
                # Search for jobs
                job_urls = scraper.search_jobs(
                    keywords=config['keywords'],
                    location=config['location'],
                    limit=config['limit']
                )
                
                search_time = time.time() - start_time
                
                scraper_result = {
                    'job_urls': job_urls,
                    'job_count': len(job_urls),
                    'search_time': round(search_time, 2),
                    'status': 'success' if job_urls else 'no_results',
                    'error': None
                }
                
                if job_urls:
                    logger.info(f"✅ {scraper_name}: {len(job_urls)} jobs found in {search_time:.1f}s")
                    config_results['successful_scrapers'] += 1
                    config_results['total_jobs'] += len(job_urls)
                    
                    # Test scraping one job for validation
                    if len(job_urls) > 0:
                        test_url = job_urls[0]
                        logger.info(f"🧪 Testing job scraping: {test_url[:60]}...")
                        
                        scrape_start = time.time()
                        job_data = scraper.scrape_job(test_url)
                        scrape_time = time.time() - scrape_start
                        
                        if job_data:
                            logger.info(f"✅ Job scraped successfully: '{job_data.title}' at '{job_data.company}' ({scrape_time:.1f}s)")
                            scraper_result['sample_job'] = {
                                'title': job_data.title,
                                'company': job_data.company,
                                'location': job_data.location,
                                'scrape_time': round(scrape_time, 2)
                            }
                        else:
                            logger.warning(f"⚠️ Job scraping failed for {test_url}")
                            scraper_result['sample_job'] = None
                else:
                    logger.warning(f"⚠️ {scraper_name}: No jobs found")
                
                config_results['scraper_results'][scraper_name] = scraper_result
                
            except Exception as e:
                logger.error(f"❌ {scraper_name} failed: {e}")
                config_results['scraper_results'][scraper_name] = {
                    'job_urls': [],
                    'job_count': 0,
                    'search_time': 0,
                    'status': 'error',
                    'error': str(e),
                    'sample_job': None
                }
            
            # Rate limiting between scrapers
            time.sleep(2)
        
        all_results.append(config_results)
        
        logger.info(f"\n📊 Configuration {i} Summary:")
        logger.info(f"   Total jobs found: {config_results['total_jobs']}")
        logger.info(f"   Successful scrapers: {config_results['successful_scrapers']}/{len(scrapers)}")
        logger.info(f"   Success rate: {(config_results['successful_scrapers']/len(scrapers)*100):.1f}%")
    
    # Final summary
    logger.info("\n" + "=" * 60)
    logger.info("🎯 FINAL MULTI-SCRAPER TEST RESULTS")
    logger.info("=" * 60)
    
    total_jobs_all_configs = sum(result['total_jobs'] for result in all_results)
    total_successful_tests = sum(result['successful_scrapers'] for result in all_results)
    total_possible_tests = len(test_configs) * len(scrapers)
    
    logger.info(f"📊 Overall Statistics:")
    logger.info(f"   Total jobs found: {total_jobs_all_configs}")
    logger.info(f"   Successful tests: {total_successful_tests}/{total_possible_tests}")
    logger.info(f"   Overall success rate: {(total_successful_tests/total_possible_tests*100):.1f}%")
    
    # Scraper performance summary
    logger.info(f"\n🏆 Scraper Performance Summary:")
    scraper_totals = {}
    for result in all_results:
        for scraper_name, scraper_data in result['scraper_results'].items():
            if scraper_name not in scraper_totals:
                scraper_totals[scraper_name] = {
                    'total_jobs': 0,
                    'successful_searches': 0,
                    'total_searches': 0,
                    'avg_search_time': 0,
                    'search_times': []
                }
            
            scraper_totals[scraper_name]['total_jobs'] += scraper_data['job_count']
            scraper_totals[scraper_name]['total_searches'] += 1
            if scraper_data['status'] == 'success':
                scraper_totals[scraper_name]['successful_searches'] += 1
            if scraper_data['search_time'] > 0:
                scraper_totals[scraper_name]['search_times'].append(scraper_data['search_time'])
    
    for scraper_name, stats in scraper_totals.items():
        success_rate = (stats['successful_searches'] / stats['total_searches'] * 100) if stats['total_searches'] > 0 else 0
        avg_time = sum(stats['search_times']) / len(stats['search_times']) if stats['search_times'] else 0
        
        logger.info(f"   {scraper_name:12}: {stats['total_jobs']:3} jobs | {success_rate:5.1f}% success | {avg_time:5.1f}s avg")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"data/results/multi_scraper_test_{timestamp}.json"
    
    import json
    from pathlib import Path
    
    # Ensure results directory exists
    Path(results_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Prepare data for JSON serialization
    json_results = {
        'test_timestamp': timestamp,
        'test_configs': test_configs,
        'scraper_names': list(scrapers.keys()),
        'results': []
    }
    
    for result in all_results:
        json_result = {
            'config': result['config'],
            'total_jobs': result['total_jobs'],
            'successful_scrapers': result['successful_scrapers'],
            'scraper_results': {}
        }
        
        for scraper_name, scraper_data in result['scraper_results'].items():
            json_result['scraper_results'][scraper_name] = {
                'job_count': scraper_data['job_count'],
                'search_time': scraper_data['search_time'],
                'status': scraper_data['status'],
                'error': scraper_data['error'],
                'sample_job': scraper_data.get('sample_job'),
                'job_urls': scraper_data['job_urls'][:3]  # Save only first 3 URLs for brevity
            }
        
        json_results['results'].append(json_result)
    
    json_results['summary'] = {
        'total_jobs_found': total_jobs_all_configs,
        'successful_tests': total_successful_tests,
        'total_possible_tests': total_possible_tests,
        'overall_success_rate': round(total_successful_tests/total_possible_tests*100, 1),
        'scraper_performance': scraper_totals
    }
    
    with open(results_file, 'w') as f:
        json.dump(json_results, f, indent=2, default=str)
    
    logger.info(f"\n💾 Results saved to: {results_file}")
    logger.info("🎉 Multi-scraper test completed!")
    
    return all_results

if __name__ == "__main__":
    test_all_scrapers()
