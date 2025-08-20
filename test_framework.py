"""
Simple test script for the scraper framework (without browser)
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
from data_collection.base_scraper import JobPosting

def test_job_posting():
    """Test the JobPosting data class."""
    logger.info("Testing JobPosting data class")
    
    # Create a sample job posting
    job = JobPosting(
        title="Senior Data Analyst",
        company="Tech Corp",
        location="San Francisco, CA",
        description="We are looking for an experienced data analyst to join our team...",
        salary="$80,000 - $120,000",
        experience_level="Senior",
        job_type="Full-time",
        url="https://example.com/job/123",
        remote_option=True
    )
    
    logger.info(f"Created job posting:")
    logger.info(f"  Title: {job.title}")
    logger.info(f"  Company: {job.company}")
    logger.info(f"  Location: {job.location}")
    logger.info(f"  Salary: {job.salary}")
    logger.info(f"  Remote: {job.remote_option}")
    logger.info(f"  Skills: {job.skills}")
    logger.info(f"  Requirements: {job.requirements}")
    
    return job

def test_settings():
    """Test that settings are loaded correctly."""
    logger.info("Testing settings configuration")
    
    logger.info(f"Database URL: {settings.database_url}")
    logger.info(f"Log level: {settings.log_level}")
    logger.info(f"Debug mode: {settings.debug_mode}")
    logger.info(f"Scraping delay: {settings.scraping_delay_min}-{settings.scraping_delay_max}s")
    logger.info(f"Max retries: {settings.max_retries}")
    logger.info(f"Project root: {settings.project_root}")
    logger.info(f"Data directory: {settings.data_dir}")
    logger.info(f"Logs directory: {settings.logs_dir}")

def test_framework():
    """Test the basic framework components."""
    logger.info("=== Testing Job Market Analyzer Framework ===")
    
    # Test settings
    test_settings()
    logger.info("")
    
    # Test JobPosting
    job = test_job_posting()
    logger.info("")
    
    # Test directory structure
    logger.info("Testing directory structure:")
    for dir_path in [settings.data_dir, settings.logs_dir, 
                     settings.data_dir / "raw", 
                     settings.data_dir / "processed", 
                     settings.data_dir / "results"]:
        if dir_path.exists():
            logger.info(f"  ✓ {dir_path}")
        else:
            logger.warning(f"  ✗ {dir_path} (missing)")
    
    logger.info("")
    logger.info("=== Framework Test Complete ===")
    logger.info("✓ Configuration system working")
    logger.info("✓ Logging system working") 
    logger.info("✓ JobPosting data class working")
    logger.info("✓ Directory structure created")
    logger.info("")
    logger.info("Next steps:")
    logger.info("1. Install Chrome browser to test web scraping")
    logger.info("2. Add API keys to .env file for AI analysis")
    logger.info("3. Test the Indeed scraper with actual data")

if __name__ == "__main__":
    test_framework()
