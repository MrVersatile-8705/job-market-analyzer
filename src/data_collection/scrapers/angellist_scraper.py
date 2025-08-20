import requests
from bs4 import BeautifulSoup
import json
import time

class AngelListScraper:
    def __init__(self):
        self.base_url = "https://angel.co/jobs"
        self.job_listings = []

    def scrape_jobs(self, num_pages=1):
        for page in range(1, num_pages + 1):
            url = f"{self.base_url}?page={page}"
            response = requests.get(url)
            if response.status_code == 200:
                self.parse_jobs(response.text)
            else:
                print(f"Failed to retrieve page {page}: {response.status_code}")
            time.sleep(2)  # Be respectful to the server

    def parse_jobs(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        job_elements = soup.find_all('div', class_='job_listing')

        for job in job_elements:
            title = job.find('h4', class_='job_title').text.strip()
            company = job.find('div', class_='company_name').text.strip()
            location = job.find('div', class_='location').text.strip()
            description = job.find('div', class_='description').text.strip()

            job_data = {
                'title': title,
                'company': company,
                'location': location,
                'description': description
            }
            self.job_listings.append(job_data)

    def save_jobs(self, filename='angellist_jobs.json'):
        with open(filename, 'w') as f:
            json.dump(self.job_listings, f, indent=4)

def scrape_angellist(num_pages=3):
    """
    Convenience function to scrape AngelList jobs and return list of job dictionaries
    
    Args:
        num_pages (int): Number of pages to scrape
        
    Returns:
        list: List of job dictionaries
    """
    scraper = AngelListScraper()
    try:
        scraper.scrape_jobs(num_pages=num_pages)
        return scraper.job_listings
    except Exception as e:
        print(f"Error scraping AngelList: {e}")
        return []

if __name__ == "__main__":
    scraper = AngelListScraper()
    scraper.scrape_jobs(num_pages=5)  # Adjust the number of pages as needed
    scraper.save_jobs()