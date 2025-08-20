"""
Comprehensive test script for the job market analyzer
"""
import sys
import json
from pathlib import Path
from datetime import datetime

# Add the src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import our modules
from config.logging_config import logger
from config.settings import settings
from data_collection.scrapers.indeed_scraper import IndeedScraper

def save_jobs_to_json(jobs, filename="scraped_jobs.json"):
    """Save scraped jobs to JSON file."""
    data_dir = Path("data/raw")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Convert JobPosting objects to dictionaries
    jobs_data = []
    for job in jobs:
        job_dict = {
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "description": job.description[:1000] + "..." if len(job.description) > 1000 else job.description,
            "salary": job.salary,
            "experience_level": job.experience_level,
            "job_type": job.job_type,
            "posted_date": job.posted_date.isoformat() if job.posted_date else None,
            "url": job.url,
            "source": job.source,
            "remote_option": job.remote_option,
            "scraped_at": datetime.now().isoformat()
        }
        jobs_data.append(job_dict)
    
    # Save to file
    filepath = data_dir / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(jobs_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Saved {len(jobs_data)} jobs to {filepath}")
    return filepath

def comprehensive_test():
    """Run a comprehensive test of the job scraper."""
    logger.info("Starting comprehensive job scraper test")
    
    # Test different job types
    test_cases = [
        {
            "keywords": ["data analyst", "business analyst"],
            "location": "Remote",
            "limit": 5,
            "description": "Remote Data/Business Analyst positions"
        },
        {
            "keywords": ["data scientist", "machine learning engineer"],
            "location": "New York, NY",
            "limit": 3,
            "description": "NYC Data Science positions"
        }
    ]
    
    all_jobs = []
    
    for i, test_case in enumerate(test_cases, 1):
        logger.info(f"\n--- Test Case {i}: {test_case['description']} ---")
        
        try:
            with IndeedScraper() as scraper:
                jobs = scraper.scrape_jobs(
                    keywords=test_case["keywords"],
                    location=test_case["location"],
                    limit=test_case["limit"]
                )
                
                logger.info(f"Successfully scraped {len(jobs)} jobs")
                
                # Display summary of each job
                for j, job in enumerate(jobs, 1):
                    logger.info(f"\nJob {j}:")
                    logger.info(f"  Title: {job.title}")
                    logger.info(f"  Company: {job.company}")
                    logger.info(f"  Location: {job.location}")
                    logger.info(f"  Remote: {job.remote_option}")
                    logger.info(f"  Salary: {job.salary}")
                    logger.info(f"  URL: {job.url}")
                
                all_jobs.extend(jobs)
                
        except Exception as e:
            logger.error(f"Test case {i} failed: {e}")
    
    # Save all jobs to JSON
    if all_jobs:
        save_jobs_to_json(all_jobs)
        
        # Print summary statistics
        logger.info(f"\n--- SUMMARY STATISTICS ---")
        logger.info(f"Total jobs scraped: {len(all_jobs)}")
        
        # Count by source
        sources = {}
        for job in all_jobs:
            sources[job.source] = sources.get(job.source, 0) + 1
        logger.info(f"Jobs by source: {sources}")
        
        # Count remote jobs
        remote_jobs = sum(1 for job in all_jobs if job.remote_option)
        logger.info(f"Remote jobs: {remote_jobs}/{len(all_jobs)} ({remote_jobs/len(all_jobs)*100:.1f}%)")
        
        # Count jobs with salary info
        salary_jobs = sum(1 for job in all_jobs if job.salary)
        logger.info(f"Jobs with salary info: {salary_jobs}/{len(all_jobs)} ({salary_jobs/len(all_jobs)*100:.1f}%)")
        
        logger.info(f"\nData saved to: {Path('data/raw/scraped_jobs.json').absolute()}")
    else:
        logger.warning("No jobs were successfully scraped")

if __name__ == "__main__":
    comprehensive_test()
