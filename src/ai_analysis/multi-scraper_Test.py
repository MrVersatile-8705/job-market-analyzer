from src.data_collection.scrapers.indeed_scraper import IndeedScraper
from src.data_collection.scrapers.linkedin_scraper import LinkedInScraper
from src.ai_analysis.ai_analyzer import JobAnalyzer
from src.config.settings import settings
import json

def test_multi_scraper_with_ai():
    """Test multiple scrapers with AI analysis."""
    
    keywords = ["data analyst", "business analyst"]
    location = "Remote"
    limit_per_site = 3  # Small test
    
    all_jobs = []
    
    # Test Indeed
    print("🔍 Testing Indeed scraper...")
    with IndeedScraper() as indeed:
        indeed_jobs = indeed.scrape_jobs(keywords, location, limit_per_site)
        all_jobs.extend(indeed_jobs)
        print(f"✅ Indeed: {len(indeed_jobs)} jobs")
    
    # Test LinkedIn (if working)
    print("🔍 Testing LinkedIn scraper...")
    try:
        with LinkedInScraper() as linkedin:
            linkedin_jobs = linkedin.scrape_jobs(keywords, location, limit_per_site)
            all_jobs.extend(linkedin_jobs)
            print(f"✅ LinkedIn: {len(linkedin_jobs)} jobs")
    except Exception as e:
        print(f"❌ LinkedIn failed: {e}")
    
    print(f"\n📊 Total jobs collected: {len(all_jobs)}")
    
    # AI Analysis (if API keys available)
    if settings.openai_api_key:
        print("🤖 Running AI analysis...")
        analyzer = JobAnalyzer()
        
        for i, job in enumerate(all_jobs[:2]):  # Analyze first 2 jobs
            print(f"\nAnalyzing job {i+1}: {job.title}")
            
            # Skill extraction
            skills = analyzer.extract_skills(job.description)
            print(f"Skills found: {skills[:5]}...")  # First 5 skills
            
            # Job categorization
            category = analyzer.categorize_job(job.title, job.description)
            print(f"Category: {category}")
    
    # Save results
    job_data = [job.__dict__ for job in all_jobs]
    with open("data/multi_scraper_results.json", "w") as f:
        json.dump(job_data, f, indent=2, default=str)
    
    print(f"\n✅ Results saved to data/multi_scraper_results.json")

if __name__ == "__main__":
    test_multi_scraper_with_ai()