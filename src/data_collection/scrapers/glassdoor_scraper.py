from bs4 import BeautifulSoup
import requests
import pandas as pd

class GlassdoorScraper:
    def __init__(self, job_title, location, num_jobs=100):
        self.job_title = job_title
        self.location = location
        self.num_jobs = num_jobs
        self.base_url = "https://www.glassdoor.com/Job/jobs.htm"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def get_job_listings(self):
        job_listings = []
        params = {
            "sc.keyword": self.job_title,
            "locT": "C",
            "locId": self.location,
            "jobType": "fulltime",
            "page": 1
        }

        while len(job_listings) < self.num_jobs:
            response = requests.get(self.base_url, headers=self.headers, params=params)
            soup = BeautifulSoup(response.text, 'html.parser')
            jobs = soup.find_all('div', class_='jobContainer')

            for job in jobs:
                title = job.find('a', class_='jobLink').text.strip()
                company = job.find('div', class_='jobInfoItem jobCompany').text.strip()
                location = job.find('span', class_='jobInfoItem jobLocation').text.strip()
                salary = job.find('span', class_='salaryText').text.strip() if job.find('span', class_='salaryText') else 'N/A'
                description = job.find('div', class_='jobDescription').text.strip()

                job_listings.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "salary": salary,
                    "description": description
                })

                if len(job_listings) >= self.num_jobs:
                    break

            params["page"] += 1

        return pd.DataFrame(job_listings)

    def save_to_csv(self, filename):
        df = self.get_job_listings()
        df.to_csv(filename, index=False)

def scrape_glassdoor(job_title="Data Analyst", location="New York, NY", num_jobs=50):
    """
    Convenience function to scrape Glassdoor jobs and return list of job dictionaries
    
    Args:
        job_title (str): Job title to search for
        location (str): Location to search in
        num_jobs (int): Number of jobs to scrape
        
    Returns:
        list: List of job dictionaries
    """
    scraper = GlassdoorScraper(job_title=job_title, location=location, num_jobs=num_jobs)
    try:
        df = scraper.get_job_listings()
        return df.to_dict('records')  # Convert DataFrame to list of dictionaries
    except Exception as e:
        print(f"Error scraping Glassdoor: {e}")
        return []

# Example usage:
# scraper = GlassdoorScraper(job_title="Data Analyst", location="New York, NY", num_jobs=100)
# scraper.save_to_csv("glassdoor_jobs.csv")