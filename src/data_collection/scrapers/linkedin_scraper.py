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
    import sys
    sys.path.append("..")
    from base_scraper import BaseScraper, JobPosting

class LinkedInScraper(BaseScraper):
    """Scraper for LinkedIn job postings."""
    
    def __init__(self):
        super().__init__("LinkedIn", "https://www.linkedin.com")
        self.search_url = f"{self.base_url}/jobs/search"

    def search_jobs(self, keywords: List[str], location: str = "United States", limit: int = 1000, days_back: Optional[int] = None) -> List[str]:
        """Search for jobs on LinkedIn and return job URLs.
        
        Args:
            keywords: List of keywords to search for
            location: Location to search in
            limit: Maximum number of job URLs to return
            days_back: Number of days to look back (optional, default: no time filter)
        """
        job_urls = []
        query = " ".join(keywords)  # LinkedIn uses space-separated keywords
        
        # Set up WebDriver
        driver = self.setup_driver(headless=True)
        
        try:
            page = 0
            while len(job_urls) < limit:
                # Build search URL for LinkedIn with optional time filter
                search_params = {
                    'keywords': query,
                    'location': location,
                    'start': page * 25,  # LinkedIn shows 25 jobs per page
                    'sortBy': 'DD'  # Sort by date (most recent)
                }
                
                # Add time filter if specified
                if days_back is not None:
                    # LinkedIn time filters: 86400 (1 day), 604800 (1 week), 2592000 (1 month)
                    time_filter = 2592000 if days_back >= 30 else (604800 if days_back >= 7 else 86400)
                    search_params['f_TPR'] = f'r{time_filter}'  # LinkedIn time filter parameter
                
                url = f"{self.search_url}?" + "&".join([f"{k}={quote_plus(str(v))}" for k, v in search_params.items()])
                logger.info(f"Searching LinkedIn page {page + 1}: {url}")
                
                driver.get(url)
                self.random_delay(3, 5)  # LinkedIn needs longer delays
                
                # Wait for job results to load
                try:
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".job-search-card"))
                    )
                except TimeoutException:
                    logger.warning(f"Timeout waiting for LinkedIn job results on page {page + 1}")
                    break
                
                # Extract job URLs from current page
                job_cards = driver.find_elements(By.CSS_SELECTOR, ".job-search-card")
                
                if not job_cards:
                    logger.info("No more job cards found on LinkedIn, ending search")
                    break
                
                page_urls = []
                for card in job_cards:
                    try:
                        link_elem = card.find_element(By.CSS_SELECTOR, ".base-search-card__title a")
                        job_url = link_elem.get_attribute("href")
                        if job_url and job_url not in page_urls:
                            # Clean up LinkedIn URL parameters
                            job_url = job_url.split('?')[0]
                            page_urls.append(job_url)
                    except Exception as e:
                        logger.debug(f"Error extracting LinkedIn job URL: {e}")
                        continue
                
                job_urls.extend(page_urls)
                logger.info(f"Found {len(page_urls)} jobs on LinkedIn page {page + 1}, total: {len(job_urls)}")
                
                # Check if we've reached the limit
                if len(job_urls) >= limit:
                    job_urls = job_urls[:limit]
                    break
                
                # Check if there's a next page
                next_button = driver.find_elements(By.CSS_SELECTOR, "button[aria-label='View next page']")
                if not next_button or not next_button[0].is_enabled():
                    logger.info("No next page found on LinkedIn, ending search")
                    break
                
                page += 1
                
        except Exception as e:
            logger.error(f"Error during LinkedIn search: {e}")
        finally:
            driver.quit()
        
        logger.info(f"LinkedIn search completed. Found {len(job_urls)} job URLs")
        return job_urls
    
    def scrape_job_details(self, job_url: str) -> Optional[JobPosting]:
        """Scrape detailed job information from LinkedIn job posting."""
        driver = None
        try:
            driver = self.setup_driver(headless=True)
            driver.get(job_url)
            self.random_delay(3, 5)
            
            # Wait for the page to load
            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "h1"))
                )
            except TimeoutException:
                logger.warning(f"Timeout waiting for LinkedIn job page to load: {job_url}")
                return None
            
            # Try to click "Show more" if present
            try:
                show_more_btn = driver.find_element(By.CSS_SELECTOR, ".show-more-less-html__button")
                if show_more_btn.is_displayed():
                    driver.execute_script("arguments[0].click();", show_more_btn)
                    self.random_delay(1, 2)
            except:
                pass  # No show more button or already expanded
            
            soup = self.parse_html(driver.page_source)
            
            # Extract job title
            title_elem = soup.find("h1", class_="top-card-layout__title")
            if not title_elem:
                title_elem = soup.find("h1")
            title = title_elem.get_text(strip=True) if title_elem else ""
            
            # Extract company name
            company_elem = soup.find("a", class_="topcard__org-name-link")
            if not company_elem:
                company_elem = soup.find("span", class_="topcard__flavor")
            company = company_elem.get_text(strip=True) if company_elem else ""
            
            # Extract location
            location_elem = soup.find("span", class_="topcard__flavor--bullet")
            location = location_elem.get_text(strip=True) if location_elem else ""
            
            # Extract job description
            desc_elem = soup.find("div", class_="show-more-less-html__markup")
            if not desc_elem:
                desc_elem = soup.find("div", class_="description__text")
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
            
            if self.validate_job_posting(job):
                return job
            else:
                logger.warning(f"Invalid LinkedIn job posting from {job_url}")
                return None
                
        except Exception as e:
            logger.error(f"Error scraping LinkedIn job details from {job_url}: {e}")
            return None
        finally:
            if driver:
                driver.quit()
    
    def _extract_salary(self, soup) -> Optional[str]:
        """Extract salary information from LinkedIn job posting."""
        salary_selectors = [
            ".compensation__salary",
            ".topcard__flavor--metadata",
            ".salary-main-rail"
        ]
        
        for selector in salary_selectors:
            salary_elem = soup.select_one(selector)
            if salary_elem:
                text = salary_elem.get_text(strip=True)
                if any(indicator in text.lower() for indicator in ['$', 'salary', 'per hour', 'per year', 'annually']):
                    return text
        
        return None
    
    def _extract_job_meta(self, soup) -> tuple[Optional[str], Optional[str]]:
        """Extract job type and experience level from LinkedIn."""
        job_type = None
        experience_level = None
        
        # Look for job criteria section
        criteria_items = soup.find_all("li", class_="description__job-criteria-item")
        
        for item in criteria_items:
            header = item.find("h3")
            if header:
                header_text = header.get_text(strip=True).lower()
                value_elem = item.find("span", class_="description__job-criteria-text")
                if value_elem:
                    value = value_elem.get_text(strip=True)
                    
                    if 'employment type' in header_text:
                        job_type = value
                    elif 'seniority level' in header_text:
                        experience_level = value
        
        return job_type, experience_level
    
    def _extract_posted_date(self, soup) -> Optional[datetime]:
        """Extract and parse posting date from LinkedIn."""
        # LinkedIn doesn't always show posting dates clearly
        # This is a simplified implementation
        return None
    
    def _check_remote_option(self, description: str, location: str) -> bool:
        """Check if LinkedIn job offers remote work option."""
        remote_keywords = [
            'remote', 'work from home', 'telecommute', 'distributed',
            'anywhere', 'location independent', 'virtual', 'hybrid'
        ]
        
        text_to_check = f"{description} {location}".lower()
        return any(keyword in text_to_check for keyword in remote_keywords)

if __name__ == "__main__":
    scraper = LinkedInScraper(job_title="Data Analyst", location="United States", num_jobs=100)
    jobs = scraper.get_job_listings()
    scraper.save_to_json(jobs)