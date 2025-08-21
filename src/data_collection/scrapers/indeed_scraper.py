import re
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

class IndeedScraper(BaseScraper):
    """Scraper for Indeed job postings."""
    
    def __init__(self):
        super().__init__("Indeed", "https://www.indeed.com")
        self.search_url = f"{self.base_url}/jobs"
    
    def search_jobs(self, keywords: List[str], location: str = "", limit: int = 100, days_back: Optional[int] = None) -> List[str]:
        """Search for jobs on Indeed and return job URLs.
        
        Args:
            keywords: List of keywords to search for
            location: Location to search in
            limit: Maximum number of job URLs to return
            days_back: Number of days to look back (optional, default: no time filter)
        """
        job_urls = []
        query = " OR ".join(keywords)
        
        # Set up WebDriver
        driver = self.setup_driver(headless=True)
        
        try:
            page = 0
            while len(job_urls) < limit:
                # Build search URL with optional date filter
                search_params = {
                    'q': query,
                    'l': location,
                    'start': page * 10,
                    'sort': 'date'  # Sort by most recent
                }
                
                # Add date filter if specified
                if days_back is not None:
                    search_params['fromage'] = str(days_back)  # Filter by days back (Indeed parameter)
                
                url = f"{self.search_url}?" + "&".join([f"{k}={quote_plus(str(v))}" for k, v in search_params.items()])
                logger.info(f"Searching Indeed page {page + 1}: {url}")
                
                driver.get(url)
                self.random_delay(2, 4)
                
                # Wait for job results to load
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-jk]"))
                    )
                except TimeoutException:
                    logger.warning(f"Timeout waiting for job results on page {page + 1}")
                    break
                
                # Extract job URLs from current page
                job_cards = driver.find_elements(By.CSS_SELECTOR, "[data-jk]")
                
                if not job_cards:
                    logger.info("No more job cards found, ending search")
                    break
                
                page_urls = []
                for card in job_cards:
                    try:
                        job_key = card.get_attribute("data-jk")
                        if job_key:
                            job_url = f"{self.base_url}/viewjob?jk={job_key}"
                            page_urls.append(job_url)
                    except Exception as e:
                        logger.debug(f"Error extracting job URL: {e}")
                        continue
                
                job_urls.extend(page_urls)
                logger.info(f"Found {len(page_urls)} jobs on page {page + 1}, total: {len(job_urls)}")
                
                # Check if we've reached the limit
                if len(job_urls) >= limit:
                    job_urls = job_urls[:limit]
                    break
                
                # Check if there's a next page
                next_button = driver.find_elements(By.CSS_SELECTOR, "a[aria-label='Next Page']")
                if not next_button:
                    logger.info("No next page found, ending search")
                    break
                
                page += 1
                
        except Exception as e:
            logger.error(f"Error during Indeed search: {e}")
        finally:
            driver.quit()
        
        logger.info(f"Indeed search completed. Found {len(job_urls)} job URLs")
        return job_urls
    
    def scrape_job_details(self, job_url: str) -> Optional[JobPosting]:
        """Scrape detailed job information from Indeed job posting using Selenium."""
        driver = None
        try:
            # Use Selenium instead of HTTP requests since Indeed blocks direct requests
            driver = self.setup_driver(headless=True)
            driver.get(job_url)
            self.random_delay(2, 4)
            
            # Wait for the page to load
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "h1"))
                )
            except TimeoutException:
                logger.warning(f"Timeout waiting for job page to load: {job_url}")
                return None
            
            # Get page source and parse with BeautifulSoup
            soup = self.parse_html(driver.page_source)
            
            # Extract job title
            title_elem = soup.find("h1", class_="jobsearch-JobInfoHeader-title")
            if not title_elem:
                title_elem = soup.find("h1")
            title = title_elem.get_text(strip=True) if title_elem else ""
            
            # Extract company name
            company_elem = soup.find("div", {"data-testid": "inlineHeader-companyName"})
            if not company_elem:
                company_elem = soup.find("span", class_="jobsearch-InlineCompanyRating")
            if not company_elem:
                company_elem = soup.find("a", {"data-testid": "company-name"})
            company = company_elem.get_text(strip=True) if company_elem else ""
            
            # Extract location
            location_elem = soup.find("div", {"data-testid": "job-location"})
            if not location_elem:
                location_elem = soup.find("div", class_="jobsearch-InlineCompanyRating")
            location = location_elem.get_text(strip=True) if location_elem else ""
            
            # Extract job description
            desc_elem = soup.find("div", {"id": "jobDescriptionText"})
            if not desc_elem:
                desc_elem = soup.find("div", class_="jobsearch-jobDescriptionText")
            description = desc_elem.get_text(strip=True) if desc_elem else ""
            
            # Extract salary information
            salary = self._extract_salary(soup)
            
            # Extract job type and experience level
            job_type, experience_level = self._extract_job_meta(soup)
            
            # Extract posted date
            posted_date = self._extract_posted_date(soup)
            
            # Check for remote work option
            remote_option = self._check_remote_option(description, location)
            
            # Create job posting object
            job = JobPosting(
                title=title,
                company=company,
                location=location,
                description=description,
                salary=salary,
                experience_level=experience_level,
                job_type=job_type,
                posted_date=posted_date,
                url=job_url,
                remote_option=remote_option
            )
            
            # Validate the job posting
            if self.validate_job_posting(job):
                return job
            else:
                logger.warning(f"Invalid job posting from {job_url}")
                return None
                
        except Exception as e:
            logger.error(f"Error scraping job details from {job_url}: {e}")
            return None
        finally:
            if driver:
                driver.quit()
    
    def _extract_salary(self, soup) -> Optional[str]:
        """Extract salary information from job posting."""
        salary_selectors = [
            ".jobsearch-JobMetadataHeader-item",
            ".icl-u-xs-mr--xs",
            "[data-testid='job-salary']",
            ".salary"
        ]
        
        for selector in salary_selectors:
            salary_elem = soup.select_one(selector)
            if salary_elem:
                text = salary_elem.get_text(strip=True)
                if any(indicator in text.lower() for indicator in ['$', 'salary', 'per hour', 'per year', 'annually']):
                    return text
        
        return None
    
    def _extract_job_meta(self, soup) -> tuple[Optional[str], Optional[str]]:
        """Extract job type and experience level."""
        job_type = None
        experience_level = None
        
        # Look for job metadata
        meta_items = soup.find_all("div", class_="jobsearch-JobMetadataHeader-item")
        
        for item in meta_items:
            text = item.get_text(strip=True).lower()
            
            # Job type detection
            if any(jt in text for jt in ['full-time', 'part-time', 'contract', 'temporary', 'internship']):
                job_type = text.title()
            
            # Experience level detection
            if any(exp in text for exp in ['entry', 'junior', 'senior', 'lead', 'principal']):
                experience_level = text.title()
        
        return job_type, experience_level
    
    def _extract_posted_date(self, soup) -> Optional[datetime]:
        """Extract and parse posting date."""
        date_elem = soup.find("span", class_="jobsearch-JobMetadataDateRange")
        if not date_elem:
            return None
        
        date_text = date_elem.get_text(strip=True).lower()
        
        try:
            if 'today' in date_text:
                return datetime.now()
            elif 'yesterday' in date_text:
                return datetime.now() - timedelta(days=1)
            elif 'days ago' in date_text:
                days = re.search(r'(\d+)', date_text)
                if days:
                    return datetime.now() - timedelta(days=int(days.group(1)))
            elif 'weeks ago' in date_text:
                weeks = re.search(r'(\d+)', date_text)
                if weeks:
                    return datetime.now() - timedelta(weeks=int(weeks.group(1)))
        except Exception as e:
            logger.debug(f"Error parsing date '{date_text}': {e}")
        
        return None
    
    def _check_remote_option(self, description: str, location: str) -> bool:
        """Check if job offers remote work option."""
        remote_keywords = [
            'remote', 'work from home', 'telecommute', 'distributed team',
            'anywhere', 'location independent', 'virtual'
        ]
        
        text_to_check = f"{description} {location}".lower()
        return any(keyword in text_to_check for keyword in remote_keywords)