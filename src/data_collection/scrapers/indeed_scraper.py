import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

class IndeedScraper:
    def __init__(self, job_title, location, num_jobs=100):
        self.job_title = job_title
        self.location = location
        self.num_jobs = num_jobs
        self.base_url = "https://www.indeed.com/jobs"
        self.job_data = []

    def scrape(self):
        for start in range(0, self.num_jobs, 10):
            url = f"{self.base_url}?q={self.job_title}&l={self.location}&start={start}"
            response = requests.get(url)
            if response.status_code == 200:
                self.parse(response.text)
            else:
                print(f"Failed to retrieve data from Indeed: {response.status_code}")
            time.sleep(1)  # Be respectful to the server

    def parse(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        job_cards = soup.find_all('div', class_='jobsearch-SerpJobCard')
        
        for job in job_cards:
            title = job.find('h2', class_='title').text.strip()
            company = job.find('span', class_='company').text.strip()
            location = job.find('div', class_='location').text.strip() if job.find('div', class_='location') else 'N/A'
            summary = job.find('div', class_='summary').text.strip()
            self.job_data.append({
                'title': title,
                'company': company,
                'location': location,
                'summary': summary
            })

    def to_dataframe(self):
        return pd.DataFrame(self.job_data)

# Convenience function for main.py integration
def scrape_indeed(job_title='Data Analyst', location='New York', num_jobs=50):
    """
    Convenience function to scrape Indeed jobs and return list of job dictionaries
    
    Args:
        job_title (str): Job title to search for
        location (str): Location to search in
        num_jobs (int): Number of jobs to scrape
        
    Returns:
        list: List of job dictionaries
    """
    scraper = IndeedScraper(job_title=job_title, location=location, num_jobs=num_jobs)
    try:
        scraper.scrape()
        return scraper.job_data
    except Exception as e:
        print(f"Error scraping Indeed: {e}")
        return []

# Example usage:
# scraper = IndeedScraper(job_title='Data Analyst', location='New York', num_jobs=100)
# scraper.scrape()
# df = scraper.to_dataframe()
# print(df.head())

# Or use the convenience function:
# jobs = scrape_indeed('Data Analyst', 'New York', 50)