import re
import time
from typing import List, Optional
from datetime import datetime, timedelta
from urllib.parse import urljoin, quote_plus
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from loguru import logger

try:
    from ..base_scraper import BaseScraper, JobPosting
except ImportError:
    # Fallback import
    import sys
    sys.path.append("..")
    from base_scraper import BaseScraper, JobPosting

class DiceScraper(BaseScraper):
    """Scraper for Dice.com job postings."""
    
    def __init__(self):
        super().__init__("Dice", "https://www.dice.com")
        self.search_url = f"{self.base_url}/jobs"
    
    def search_jobs(self, keywords: List[str], location: str = "", limit: int = 100, days_back: Optional[int] = None) -> List[str]:
        """Search for jobs on Dice and return job URLs.
        
        Args:
            keywords: List of keywords to search for
            location: Location to search in
            limit: Maximum number of job URLs to return
            days_back: Number of days to look back (optional)
        """
        job_urls = []
        query = " OR ".join(keywords)
        
        # Set up WebDriver
        driver = self.setup_driver(headless=True)
        
        try:
            page = 1
            while len(job_urls) < limit:
                # Build search URL
                search_params = f"q={quote_plus(query)}&location={quote_plus(location)}&page={page}"
                if days_back:
                    # Dice uses posted date filter
                    search_params += f"&postedDate={days_back}"
                
                url = f"{self.search_url}?{search_params}"
                
                logger.info(f"Searching Dice page {page}: {url}")
                driver.get(url)
                
                # Wait for job listings to load
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-cy='search-result-title'] a, .card-title a"))
                    )
                except TimeoutException:
                    logger.warning(f"No job listings found on page {page}")
                    break
                
                # Extract job URLs from this page
                job_elements = driver.find_elements(By.CSS_SELECTOR, "[data-cy='search-result-title'] a, .card-title a, .card-title-link")
                
                if not job_elements:
                    logger.warning(f"No job elements found on page {page}")
                    break
                
                page_urls = []
                for element in job_elements:
                    try:
                        job_url = element.get_attribute('href')
                        if job_url and job_url not in job_urls:
                            # Ensure full URL
                            if job_url.startswith('/'):
                                job_url = urljoin(self.base_url, job_url)
                            job_urls.append(job_url)
                            page_urls.append(job_url)
                            
                            if len(job_urls) >= limit:
                                break
                    except Exception as e:
                        logger.error(f"Error extracting job URL: {e}")
                        continue
                
                logger.info(f"Found {len(page_urls)} job URLs on page {page} (Total: {len(job_urls)})")
                
                if len(page_urls) == 0:
                    logger.info("No more jobs found, stopping search")
                    break
                
                page += 1
                
                # Rate limiting
                time.sleep(self.get_delay())
                
        except Exception as e:
            logger.error(f"Error during Dice search: {e}")
        finally:
            driver.quit()
        
        logger.info(f"Dice search completed: {len(job_urls)} job URLs found")
        return job_urls[:limit]
    
    def scrape_job_details(self, job_url: str) -> Optional[JobPosting]:
        """Scrape detailed job information from a Dice job URL."""
        
        driver = self.setup_driver(headless=True)
        
        try:
            logger.debug(f"Scraping Dice job: {job_url}")
            driver.get(job_url)
            
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "main"))
            )
            
            # Extract job information
            job_data = {
                'url': job_url,
                'source': self.name,
                'title': '',
                'company': '',
                'location': '',
                'description': '',
                'salary': None,
                'experience_level': None,
                'job_type': None,
                'posted_date': None
            }
            
            # Job title
            try:
                title_element = driver.find_element(By.CSS_SELECTOR, "h1[data-cy='jobTitle'], .jobTitle h1, h1.job-title")
                job_data['title'] = title_element.text.strip()
            except NoSuchElementException:
                logger.warning("Job title not found")
            
            # Company name
            try:
                company_element = driver.find_element(By.CSS_SELECTOR, "[data-cy='companyName'] a, .company-name a, .employer-name")
                job_data['company'] = company_element.text.strip()
            except NoSuchElementException:
                try:
                    # Alternative selector
                    company_element = driver.find_element(By.CSS_SELECTOR, "[data-cy='companyName'], .company-name")
                    job_data['company'] = company_element.text.strip()
                except NoSuchElementException:
                    logger.warning("Company name not found")
            
            # Location
            try:
                location_element = driver.find_element(By.CSS_SELECTOR, "[data-cy='jobLocation'], .location, .job-location")
                job_data['location'] = location_element.text.strip()
            except NoSuchElementException:
                logger.warning("Location not found")
            
            # Salary
            try:
                salary_element = driver.find_element(By.CSS_SELECTOR, "[data-cy='salary'], .salary, .compensation-text")
                job_data['salary'] = salary_element.text.strip()
            except NoSuchElementException:
                logger.debug("Salary not found")
            
            # Job description
            try:
                description_element = driver.find_element(By.CSS_SELECTOR, "[data-cy='jobDescription'], .job-description, .description")
                job_data['description'] = description_element.text.strip()
            except NoSuchElementException:
                logger.warning("Job description not found")
            
            # Experience level
            try:
                exp_elements = driver.find_elements(By.CSS_SELECTOR, "[data-cy='experience'], .experience-level, .seniority")
                if exp_elements:
                    job_data['experience_level'] = exp_elements[0].text.strip()
            except NoSuchElementException:
                logger.debug("Experience level not found")
            
            # Job type
            try:
                job_type_elements = driver.find_elements(By.CSS_SELECTOR, "[data-cy='employmentType'], .employment-type, .job-type")
                if job_type_elements:
                    job_data['job_type'] = job_type_elements[0].text.strip()
            except NoSuchElementException:
                logger.debug("Job type not found")
            
            # Posted date
            try:
                date_element = driver.find_element(By.CSS_SELECTOR, "[data-cy='postedDate'], .posted-date, .post-date")
                date_text = date_element.text.strip()
                job_data['posted_date'] = self.parse_date(date_text)
            except NoSuchElementException:
                logger.debug("Posted date not found")
            
            # Create JobPosting object
            if job_data['title'] and job_data['company']:
                return JobPosting(**job_data)
            else:
                logger.warning(f"Missing essential job data for {job_url}")
                return None
                
        except Exception as e:
            logger.error(f"Error scraping Dice job {job_url}: {e}")
            return None
        finally:
            driver.quit()
    
    def parse_date(self, date_text: str) -> Optional[datetime]:
        """Parse Dice date formats."""
        if not date_text:
            return None
        
        date_text = date_text.lower().strip()
        now = datetime.now()
        
        try:
            # Handle "X days ago", "X hours ago", etc.
            if 'day' in date_text:
                days = int(re.search(r'(\d+)', date_text).group(1))
                return now - timedelta(days=days)
            elif 'hour' in date_text:
                hours = int(re.search(r'(\d+)', date_text).group(1))
                return now - timedelta(hours=hours)
            elif 'week' in date_text:
                weeks = int(re.search(r'(\d+)', date_text).group(1))
                return now - timedelta(weeks=weeks)
            elif 'month' in date_text:
                months = int(re.search(r'(\d+)', date_text).group(1))
                return now - timedelta(days=months * 30)
            elif 'today' in date_text:
                return now
            elif 'yesterday' in date_text:
                return now - timedelta(days=1)
            elif 'posted' in date_text and 'ago' in date_text:
                # Try to extract number and unit
                match = re.search(r'(\d+)\s*(day|hour|week|month)', date_text)
                if match:
                    num = int(match.group(1))
                    unit = match.group(2)
                    if unit == 'day':
                        return now - timedelta(days=num)
                    elif unit == 'hour':
                        return now - timedelta(hours=num)
                    elif unit == 'week':
                        return now - timedelta(weeks=num)
                    elif unit == 'month':
                        return now - timedelta(days=num * 30)
            return None
        except (AttributeError, ValueError):
            logger.warning(f"Could not parse date: {date_text}")
            return None

def scrape_dice(keywords: List[str] = None, location: str = "", limit: int = 50) -> List[JobPosting]:
    """Convenience function to scrape Dice jobs."""
    if keywords is None:
        keywords = ["Data Analyst", "Data Scientist", "Data Engineer", "Business Intelligence"]
    
    scraper = DiceScraper()
    job_urls = scraper.search_jobs(keywords, location, limit)
    
    jobs = []
    for url in job_urls:
        job = scraper.scrape_job_details(url)
        if job:
            jobs.append(job)
    
    return jobs
