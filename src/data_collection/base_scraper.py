import time
import random
import requests
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from loguru import logger

# Import settings - will work when run from the project directory
try:
    # Try different import paths based on how the script is being executed
    try:
        from sqaZ import settings  # When executed as part of the package
    except ImportError:
        try:
            from ..config.settings import settings  # If config is one level up
        except ImportError:
            # Try absolute import
            from config.settings import settings
except ImportError:
    # Fallback for when imports don't work
    class MockSettings:
        scraping_delay_min = 1
        scraping_delay_max = 3
        max_retries = 3
    settings = MockSettings()

@dataclass
class JobPosting:
    """Data class for job posting information."""
    title: str
    company: str
    location: str
    description: str
    salary: Optional[str] = None
    experience_level: Optional[str] = None
    job_type: Optional[str] = None
    posted_date: Optional[datetime] = None
    url: str = ""
    source: str = ""
    skills: List[str] = None
    requirements: List[str] = None
    benefits: List[str] = None
    remote_option: bool = False
    
    def __post_init__(self):
        if self.skills is None:
            self.skills = []
        if self.requirements is None:
            self.requirements = []
        if self.benefits is None:
            self.benefits = []

class BaseScraper(ABC):
    """Base class for all job site scrapers."""
    
    def __init__(self, site_name: str, base_url: str):
        self.site_name = site_name
        self.base_url = base_url
        self.session = requests.Session()
        self.driver = None
        self.scraped_jobs = []
        self.failed_urls = []
        
        # Set up session headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        logger.info(f"Initialized {self.site_name} scraper")
    
    def setup_driver(self, headless: bool = True) -> webdriver.Chrome:
        """Set up Chrome WebDriver with optimal settings."""
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Add user agent
        chrome_options.add_argument(f"--user-agent={self.session.headers['User-Agent']}")
        
        # Use webdriver-manager to automatically handle ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        self.driver = driver
        logger.info(f"WebDriver initialized for {self.site_name}")
        return driver
    
    def random_delay(self, min_delay: Optional[float] = None, max_delay: Optional[float] = None):
        """Add random delay between requests to avoid being blocked."""
        min_delay = min_delay or settings.scraping_delay_min
        max_delay = max_delay or settings.scraping_delay_max
        delay = random.uniform(min_delay, max_delay)
        logger.debug(f"Sleeping for {delay:.2f} seconds")
        time.sleep(delay)
    
    def make_request(self, url: str, retries: int = None) -> Optional[requests.Response]:
        """Make HTTP request with retry logic."""
        retries = retries or settings.max_retries
        
        for attempt in range(retries + 1):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                logger.debug(f"Successfully fetched {url}")
                return response
            
            except requests.exceptions.RequestException as e:
                logger.warning(f"Request failed for {url} (attempt {attempt + 1}/{retries + 1}): {e}")
                if attempt < retries:
                    self.random_delay(2, 5)  # Longer delay on retry
                else:
                    logger.error(f"Failed to fetch {url} after {retries + 1} attempts")
                    self.failed_urls.append(url)
                    return None
    
    def parse_html(self, html_content: str) -> BeautifulSoup:
        """Parse HTML content using BeautifulSoup."""
        return BeautifulSoup(html_content, 'lxml')
    
    @abstractmethod
    def search_jobs(self, keywords: List[str], location: str = "", limit: int = 100) -> List[str]:
        """Search for jobs and return list of job URLs."""
        pass
    
    @abstractmethod
    def scrape_job_details(self, job_url: str) -> Optional[JobPosting]:
        """Scrape detailed information from a job posting URL."""
        pass
    
    def scrape_jobs(self, keywords: List[str], location: str = "", limit: int = 100) -> List[JobPosting]:
        """Main method to scrape jobs from the site."""
        logger.info(f"Starting to scrape {self.site_name} for keywords: {keywords}, location: {location}, limit: {limit}")
        
        # Get job URLs
        job_urls = self.search_jobs(keywords, location, limit)
        logger.info(f"Found {len(job_urls)} job URLs from {self.site_name}")
        
        # Scrape details for each job
        jobs = []
        for i, url in enumerate(job_urls):
            logger.info(f"Scraping job {i+1}/{len(job_urls)}: {url}")
            
            job = self.scrape_job_details(url)
            if job:
                job.source = self.site_name
                jobs.append(job)
                logger.debug(f"Successfully scraped job: {job.title} at {job.company}")
            else:
                logger.warning(f"Failed to scrape job details from {url}")
            
            # Add delay between requests
            if i < len(job_urls) - 1:  # Don't delay after the last job
                self.random_delay()
        
        logger.info(f"Successfully scraped {len(jobs)} jobs from {self.site_name}")
        self.scraped_jobs.extend(jobs)
        return jobs
    
    def validate_job_posting(self, job: JobPosting) -> bool:
        """Validate that a job posting has required fields."""
        required_fields = ['title', 'company', 'description']
        
        for field in required_fields:
            if not getattr(job, field) or not getattr(job, field).strip():
                logger.warning(f"Job posting missing required field: {field}")
                return False
        
        return True
    
    def cleanup(self):
        """Clean up resources."""
        if self.driver:
            self.driver.quit()
            logger.info(f"WebDriver closed for {self.site_name}")
        
        if self.session:
            self.session.close()
            logger.info(f"Session closed for {self.site_name}")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
