from data_collection.scrapers.linkedin_scraper import scrape_linkedin
from data_collection.scrapers.indeed_scraper import scrape_indeed
from data_collection.scrapers.glassdoor_scraper import scrape_glassdoor
from data_collection.scrapers.angellist_scraper import scrape_angellist
from data_collection.data_validator import validate_data
from data_collection.deduplicator import remove_duplicates
from data_processing.text_processor import process_text
from data_processing.skill_extractor import extract_skills
from data_processing.salary_parser import parse_salaries
from data_processing.nlp_analyzer import analyze_nlp
from ai_analysis.openai_client import analyze_with_openai
from ai_analysis.claude_client import analyze_with_claude
from statistical_analysis.salary_analyzer import analyze_salary_trends
from statistical_analysis.trend_analyzer import identify_trends
from visualization.dashboard import create_dashboard
from visualization.report_generator import generate_report
from config.job_search_config import get_all_job_titles, get_enhanced_configs
import os

def main():
    # Step 1: Data Collection
    print("Collecting job data...")
    linkedin_data = scrape_linkedin()
    indeed_data = scrape_indeed()
    glassdoor_data = scrape_glassdoor()
    angellist_data = scrape_angellist()

    # Step 2: Data Validation
    print("Validating data...")
    all_data = linkedin_data + indeed_data + glassdoor_data + angellist_data
    valid_data = validate_data(all_data)

    # Step 3: Deduplication
    print("Removing duplicates...")
    unique_data = remove_duplicates(valid_data)

    # Step 4: Data Processing
    print("Processing text data...")
    processed_data = process_text(unique_data)
    skills = extract_skills(processed_data)
    salaries = parse_salaries(processed_data)
    nlp_analysis = analyze_nlp(processed_data)

    # Step 5: AI Analysis
    print("Performing AI analysis...")
    openai_results = analyze_with_openai(processed_data)
    claude_results = analyze_with_claude(processed_data)

    # Step 6: Statistical Analysis
    print("Analyzing salary trends...")
    salary_trends = analyze_salary_trends(salaries)
    trends = identify_trends(processed_data)

    # Step 7: Visualization
    print("Creating dashboard...")
    dashboard = create_dashboard(salary_trends, trends)
    
    # Step 8: Report Generation
    print("Generating report...")
    report = generate_report(dashboard)

    # Step 9: Save results
    output_dir = 'data/results'
    os.makedirs(output_dir, exist_ok=True)
    report.save(os.path.join(output_dir, 'job_market_analysis_report.pdf'))

    print("Job market analysis completed successfully!")

if __name__ == "__main__":
    main()