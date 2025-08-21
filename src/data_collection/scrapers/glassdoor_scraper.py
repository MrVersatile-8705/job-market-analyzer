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

class GlassdoorScraper(BaseScraper):
    """Scraper for Glassdoor job postings."""
    
    def __init__(self):
        super().__init__("Glassdoor", "https://www.glassdoor.com")
        self.search_url = f"{self.base_url}/Job/jobs.htm"
    
    def search_jobs(self, keywords: List[str], location: str = "", limit: int = 100) -> List[str]:
        """Search for jobs on Glassdoor and return job URLs."""
        job_urls = []
        query = " ".join(keywords)
        
        # Set up WebDriver
        driver = self.setup_driver(headless=True)
        
        try:
            page = 1
            while len(job_urls) < limit:
                # Build search URL for Glassdoor
                search_params = {
                    'sc.keyword': query,
                    'locT': 'C',
                    'locId': location,
                    'jobType': 'fulltime',
                    'p': page
                }
                
                url = f"{self.search_url}?" + "&".join([f"{k}={quote_plus(str(v))}" for k, v in search_params.items()])
                logger.info(f"Searching Glassdoor page {page}: {url}")
                
                driver.get(url)
                self.random_delay(3, 5)
                
                # Wait for job results to load
                try:
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='job-link']"))
                    )
                except TimeoutException:
                    logger.warning(f"Timeout waiting for Glassdoor job results on page {page}")
                    break
                
                # Extract job URLs from current page
                job_links = driver.find_elements(By.CSS_SELECTOR, "[data-test='job-link']")
                
                if not job_links:
                    logger.info("No more job links found on Glassdoor, ending search")
                    break
                
                page_urls = []
                for link in job_links:
                    try:
                        job_url = link.get_attribute("href")
                        if job_url and job_url not in page_urls:
                            # Clean up Glassdoor URL parameters
                            job_url = job_url.split('?')[0]
                            page_urls.append(job_url)
                    except Exception as e:
                        logger.debug(f"Error extracting Glassdoor job URL: {e}")
                        continue
                
                job_urls.extend(page_urls)
                logger.info(f"Found {len(page_urls)} jobs on Glassdoor page {page}, total: {len(job_urls)}")
                
                # Check if we've reached the limit
                if len(job_urls) >= limit:
                    job_urls = job_urls[:limit]
                    break
                
                # Check if there's a next page
                next_button = driver.find_elements(By.CSS_SELECTOR, "[data-test='pagination-next']")
                if not next_button or not next_button[0].is_enabled():
                    logger.info("No next page found on Glassdoor, ending search")
                    break
                
                page += 1
                
        except Exception as e:
            logger.error(f"Error during Glassdoor search: {e}")
        finally:
            driver.quit()
        
        logger.info(f"Glassdoor search completed. Found {len(job_urls)} job URLs")
        return job_urls
    
    def scrape_job_details(self, job_url: str) -> Optional[JobPosting]:
        """Scrape detailed job information from Glassdoor job posting."""
        driver = None
        try:
            driver = self.setup_driver(headless=True)
            driver.get(job_url)
            self.random_delay(3, 5)
            
            # Wait for the page to load
            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='job-title']"))
                )
            except TimeoutException:
                logger.warning(f"Timeout waiting for Glassdoor job page to load: {job_url}")
                return None
            
            soup = self.parse_html(driver.page_source)
            
            # Extract job title
            title_elem = soup.find(attrs={"data-test": "job-title"})
            title = title_elem.get_text(strip=True) if title_elem else ""
            
            # Extract company name
            company_elem = soup.find(attrs={"data-test": "employer-name"})
            company = company_elem.get_text(strip=True) if company_elem else ""
            
            # Extract location
            location_elem = soup.find(attrs={"data-test": "job-location"})
            location = location_elem.get_text(strip=True) if location_elem else ""
            
            # Extract job description
            desc_elem = soup.find(attrs={"data-test": "jobDescriptionContent"})
            if not desc_elem:
                desc_elem = soup.find("div", class_="jobDescriptionContent")
            description = desc_elem.get_text(strip=True) if desc_elem else ""
            
            # Extract salary information
            salary = self._extract_salary(soup)
            
            # Extract job type and experience level
            job_type, experience_level = self._extract_job_meta(soup, description)
            
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
                logger.warning(f"Invalid Glassdoor job posting from {job_url}")
                return None
                
        except Exception as e:
            logger.error(f"Error scraping Glassdoor job details from {job_url}: {e}")
            return None
        finally:
            if driver:
                driver.quit()
    
    def _extract_salary(self, soup) -> Optional[str]:
        """Extract salary information from Glassdoor job posting."""
        salary_selectors = [
            "[data-test='salary-estimate']",
            ".salary-estimate",
            ".salaryText"
        ]
        
        for selector in salary_selectors:
            salary_elem = soup.select_one(selector)
            if salary_elem:
                text = salary_elem.get_text(strip=True)
                if any(indicator in text.lower() for indicator in ['$', 'salary', 'per hour', 'per year', 'annually']):
                    return text
        
        return None
    
    def _extract_job_meta(self, soup, description: str) -> tuple[Optional[str], Optional[str]]:
        """Extract job type and experience level from Glassdoor."""
        job_type = None
        experience_level = None
        
        # Look for job metadata in various sections
        meta_sections = soup.find_all("div", class_="css-1cnx9l4")
        
        for section in meta_sections:
            text = section.get_text(strip=True).lower()
            if 'full-time' in text or 'part-time' in text or 'contract' in text:
                job_type = section.get_text(strip=True)
            elif 'entry' in text or 'senior' in text or 'junior' in text or 'mid' in text:
                experience_level = section.get_text(strip=True)
        
        # Fallback: extract from description
        if not experience_level:
            desc_lower = description.lower()
            if any(level in desc_lower for level in ['entry level', 'junior', 'associate']):
                experience_level = "Entry Level"
            elif any(level in desc_lower for level in ['senior', 'lead', 'principal']):
                experience_level = "Senior Level"
            elif any(level in desc_lower for level in ['mid', 'intermediate']):
                experience_level = "Mid Level"
        
        return job_type, experience_level
    
    def _extract_posted_date(self, soup) -> Optional[datetime]:
        """Extract and parse posting date from Glassdoor."""
        date_elem = soup.find(attrs={"data-test": "job-posted-date"})
        if not date_elem:
            date_elem = soup.find("div", class_="css-1cnx9l4")
        
        if date_elem:
            date_text = date_elem.get_text(strip=True).lower()
            try:
                if "today" in date_text:
                    return datetime.now()
                elif "yesterday" in date_text:
                    return datetime.now() - timedelta(days=1)
                elif "days ago" in date_text:
                    days = int(re.search(r'(\d+)', date_text).group(1))
                    return datetime.now() - timedelta(days=days)
            except:
                pass
        
        return None
    
    def _check_remote_option(self, description: str, location: str) -> bool:
        """Check if Glassdoor job offers remote work option."""
        remote_keywords = [
            'remote', 'work from home', 'telecommute', 'distributed',
            'anywhere', 'location independent', 'virtual', 'hybrid'
        ]
        
        text_to_check = f"{description} {location}".lower()
        return any(keyword in text_to_check for keyword in remote_keywords)

if __name__ == "__main__":
    # Test the scraper
    scraper = GlassdoorScraper()
    job_urls = scraper.search_jobs(["Data Analyst"], "New York", limit=5)
    print(f"Found {len(job_urls)} job URLs")