#!/usr/bin/env python3
"""
Scaled Test - Medium Dataset
Now that focused test works, let's process more jobs
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from loguru import logger
from focused_test import focused_test

# Configure logging
logger.remove()
logger.add(sys.stdout, level="INFO")

def scaled_test():
    """Run a medium-scale test with more jobs."""
    
    logger.info("🚀 Medium-Scale Test")
    logger.info("=" * 50)
    
    # Test scenarios with increased limits
    test_cases = [
        {
            "name": "Remote Data Analysts - Full Stack",
            "keywords": ["Data Analyst", "Business Intelligence Analyst","Strategic Analyst", "Remote"],
            "location": "",
            "limit": 30,  # Increased from 3
            "days_back": 30,
            "expected_skills": ["SQL", "Python", "Excel", "Tableau", "Power BI"]
        },
        {
            "name": "Business Intelligence - Tech Hubs",
            "keywords": ["Business Intelligence", "BI Developer"],
            "location": "Cleveland, OH",
            "limit": 30,  # Increased from 2
            "days_back": 30,
            "expected_skills": ["Power BI", "Tableau", "SQL", "Data Warehouse"]
        },
        {
            "name": "Data Science - Mid Level",
            "keywords": ["Data Scientist", "Senior Data Scientist"],
            "location": "New York, NY",
            "limit": 30,
            "days_back": 30,
            "expected_skills": ["Python", "Machine Learning", "Statistics", "R"]
        }
    ]
    
    logger.info(f"📊 Planning to process ~33 jobs across 3 scenarios")
    logger.info("⏱️ Estimated time: 30-20 minutes")
    
    proceed = input("\nProceed with medium-scale test? (y/n): ")
    if proceed.lower() != 'y':
        logger.info("Test cancelled by user")
        return
    
    # Use the existing focused_test framework with new parameters
    # This would require modifying focused_test to accept parameters
    logger.info("🎯 Starting scaled data collection...")
    
if __name__ == "__main__":
    scaled_test()
