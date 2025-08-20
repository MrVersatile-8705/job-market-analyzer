import unittest
from src.data_collection.scrapers.linkedin_scraper import LinkedInScraper
from src.data_collection.scrapers.indeed_scraper import IndeedScraper
from src.data_collection.scrapers.glassdoor_scraper import GlassdoorScraper
from src.data_collection.scrapers.angellist_scraper import AngelListScraper

class TestScrapers(unittest.TestCase):

    def setUp(self):
        self.linkedin_scraper = LinkedInScraper()
        self.indeed_scraper = IndeedScraper()
        self.glassdoor_scraper = GlassdoorScraper()
        self.angellist_scraper = AngelListScraper()

    def test_linkedin_scraper(self):
        job_data = self.linkedin_scraper.scrape_jobs()
        self.assertIsInstance(job_data, list)
        self.assertGreater(len(job_data), 0)

    def test_indeed_scraper(self):
        job_data = self.indeed_scraper.scrape_jobs()
        self.assertIsInstance(job_data, list)
        self.assertGreater(len(job_data), 0)

    def test_glassdoor_scraper(self):
        job_data = self.glassdoor_scraper.scrape_jobs()
        self.assertIsInstance(job_data, list)
        self.assertGreater(len(job_data), 0)

    def test_angellist_scraper(self):
        job_data = self.angellist_scraper.scrape_jobs()
        self.assertIsInstance(job_data, list)
        self.assertGreater(len(job_data), 0)

if __name__ == '__main__':
    unittest.main()