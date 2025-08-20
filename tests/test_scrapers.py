import unittest
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_collection.scrapers.linkedin_scraper import LinkedInScraper
from data_collection.scrapers.indeed_scraper import IndeedScraper
from data_collection.scrapers.glassdoor_scraper import GlassdoorScraper
from data_collection.scrapers.angellist_scraper import AngelListScraper

class TestScrapers(unittest.TestCase):

    def setUp(self):
        # Initialize scrapers with default parameters
        self.linkedin_scraper = LinkedInScraper(job_title="Data Analyst", location="United States", num_jobs=5)
        self.indeed_scraper = IndeedScraper(job_title="Data Analyst", location="New York", num_jobs=5)
        self.glassdoor_scraper = GlassdoorScraper(job_title="Data Analyst", location="New York, NY", num_jobs=5)
        self.angellist_scraper = AngelListScraper()

    def test_linkedin_scraper_initialization(self):
        """Test LinkedIn scraper can be initialized"""
        self.assertEqual(self.linkedin_scraper.job_title, "Data Analyst")
        self.assertEqual(self.linkedin_scraper.location, "United States")
        self.assertEqual(self.linkedin_scraper.num_jobs, 5)

    def test_indeed_scraper_initialization(self):
        """Test Indeed scraper can be initialized"""
        self.assertEqual(self.indeed_scraper.job_title, "Data Analyst")
        self.assertEqual(self.indeed_scraper.location, "New York")
        self.assertEqual(self.indeed_scraper.num_jobs, 5)

    def test_glassdoor_scraper_initialization(self):
        """Test Glassdoor scraper can be initialized"""
        self.assertEqual(self.glassdoor_scraper.job_title, "Data Analyst")
        self.assertEqual(self.glassdoor_scraper.location, "New York, NY")
        self.assertEqual(self.glassdoor_scraper.num_jobs, 5)

    def test_angellist_scraper_initialization(self):
        """Test AngelList scraper can be initialized"""
        self.assertIsInstance(self.angellist_scraper, AngelListScraper)
        self.assertEqual(self.angellist_scraper.base_url, "https://angel.co/jobs")

    def test_indeed_dataframe_creation(self):
        """Test Indeed scraper can create empty DataFrame"""
        df = self.indeed_scraper.to_dataframe()
        self.assertIsNotNone(df)
        # Empty DataFrame should have 0 rows initially
        self.assertEqual(len(df), 0)

if __name__ == '__main__':
    unittest.main()