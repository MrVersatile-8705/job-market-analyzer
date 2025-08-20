from bs4 import BeautifulSoup
import requests
import json
import time

class LinkedInScraper:
    def __init__(self, job_title, location, num_jobs=100):
        self.job_title = job_title
        self.location = location
        self.num_jobs = num_jobs
        self.base_url = "https://www.linkedin.com/jobs/search/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def get_job_listings(self):
        job_listings = []
        for start in range(0, self.num_jobs, 25):
            url = f"{self.base_url}?keywords={self.job_title}&location={self.location}&start={start}"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                job_cards = soup.find_all('div', class_='job-search-card')
                for job_card in job_cards:
                    job_data = self.extract_job_data(job_card)
                    if job_data:
                        job_listings.append(job_data)
            time.sleep(2)  # Respectful scraping
        return job_listings

    def extract_job_data(self, job_card):
        try:
            title = job_card.find('h3', class_='job-search-card__title').get_text(strip=True)
            company = job_card.find('h4', class_='job-search-card__subtitle').get_text(strip=True)
            location = job_card.find('span', class_='job-search-card__location').get_text(strip=True)
            job_link = job_card.find('a', class_='job-search-card__link')['href']
            return {
                'title': title,
                'company': company,
                'location': location,
                'link': job_link
            }
        except AttributeError:
            return None

    def save_to_json(self, job_listings, filename='linkedin_jobs.json'):
        with open(filename, 'w') as f:
            json.dump(job_listings, f, indent=4)

if __name__ == "__main__":
    scraper = LinkedInScraper(job_title="Data Analyst", location="United States", num_jobs=100)
    jobs = scraper.get_job_listings()
    scraper.save_to_json(jobs)