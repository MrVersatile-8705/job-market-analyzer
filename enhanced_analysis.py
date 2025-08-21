#!/usr/bin/env python3
"""
Enhanced Large-Scale Job Market Analysis
Processes 100+ jobs efficiently and creates comprehensive analytics
"""

import sys
import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from loguru import logger
from src.config.settings import Settings
from src.config.job_search_config import get_enhanced_configs, get_all_job_titles
from src.data_collection.scrapers.indeed_scraper import IndeedScraper
from src.ai_analysis.job_analyzer import AIJobAnalyzer

# Configure logging
logger.remove()
logger.add(
    "logs/enhanced_analysis.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="INFO",
    rotation="10 MB"
)
logger.add(sys.stdout, level="INFO")

def enhanced_job_analysis():
    """Run enhanced job market analysis targeting 100+ jobs."""
    
    logger.info("🚀 Enhanced Large-Scale Job Market Analysis")
    logger.info("=" * 60)
    
    # Initialize AI analyzer
    logger.info("🤖 Initializing AI components...")
    try:
        ai_analyzer = AIJobAnalyzer()
        ai_enabled = True
        logger.info("✅ AI analyzer ready")
    except Exception as e:
        logger.error(f"❌ AI initialization failed: {e}")
        ai_enabled = False
    
    # Define enhanced test scenarios for 100+ jobs
    test_scenarios = [
        {
            "name": "Remote Data Analysts - All Experience Levels",
            "keywords": ["Data Analyst", "Remote"],
            "location": "",
            "limit": 30,
            "days_back": 90,
        },
        {
            "name": "Business Intelligence - Major Tech Hubs",
            "keywords": ["Business Intelligence", "BI Analyst"],
            "location": "New York, NY",
            "limit": 25,
            "days_back": 90,
        },
        {
            "name": "Data Science US",
            "keywords": ["Data Scientist", "AI Product Manager",""],
            "location": "United States",
            "limit": 25,
            "days_back": 90,
        },
        {
            "name": "Analytics -Healthcare",
            "keywords": ["Financial Analyst", "Population Health Analyst"],
            "location": "Cleveland, OH",
            "limit": 30,
            "days_back": 30,
        }
    ]
    
    total_target = sum(scenario['limit'] for scenario in test_scenarios)
    logger.info(f"📊 Target: {total_target} jobs across {len(test_scenarios)} scenarios")
    logger.info("⏱️ Estimated time: 60-90 minutes")
    
    # Confirm before proceeding
    proceed = input(f"\nProceed with enhanced analysis ({total_target} jobs)? (y/n): ")
    if proceed.lower() != 'y':
        logger.info("Analysis cancelled by user")
        return
    
    # Process scenarios
    start_time = datetime.now()
    all_results = []
    
    for i, scenario in enumerate(test_scenarios, 1):
        logger.info(f"\n📊 Scenario {i}/{len(test_scenarios)}: {scenario['name']}")
        logger.info("-" * 50)
        
        try:
            scenario_results = process_enhanced_scenario(scenario, ai_analyzer, ai_enabled, i)
            all_results.extend(scenario_results)
            
            # Progress update
            logger.info(f"✅ Scenario {i} completed: {len(scenario_results)} jobs | Total: {len(all_results)}")
            
        except KeyboardInterrupt:
            logger.warning("Process interrupted by user")
            break
        except Exception as e:
            logger.error(f"Scenario {i} failed: {e}")
            continue
        
        # Brief pause between scenarios
        time.sleep(3)
    
    # Generate comprehensive results
    end_time = datetime.now()
    processing_time = end_time - start_time
    
    logger.info(f"\n🎉 Enhanced Analysis Complete!")
    logger.info(f"⏱️ Total processing time: {processing_time}")
    logger.info(f"📊 Total jobs collected: {len(all_results)}")
    
    # Export results and create analytics
    results_file = export_enhanced_results(all_results, processing_time)
    
    if results_file:
        logger.info("\n📈 Creating analytical dashboard...")
        create_enhanced_dashboard(results_file)

def process_enhanced_scenario(scenario, ai_analyzer, ai_enabled, scenario_num):
    """Process a single scenario with enhanced features."""
    
    # Search for jobs
    logger.info(f"🔍 Searching for {scenario['limit']} jobs...")
    scraper = IndeedScraper()
    
    job_urls = scraper.search_jobs(
        keywords=scenario['keywords'],
        location=scenario['location'],
        limit=scenario['limit'],
        days_back=scenario.get('days_back', 30)
    )
    
    if not job_urls:
        logger.warning(f"No jobs found for {scenario['name']}")
        return []
    
    logger.info(f"✅ Found {len(job_urls)} job URLs")
    
    # Process jobs with enhanced tracking
    scenario_results = []
    successful_jobs = 0
    failed_jobs = 0
    
    for j, url in enumerate(job_urls, 1):
        try:
            # Progress indicator
            if j % 10 == 0 or j == len(job_urls):
                logger.info(f"  📄 Progress: {j}/{len(job_urls)} ({(j/len(job_urls)*100):.1f}%) | Success: {successful_jobs} | Errors: {failed_jobs}")
            
            # Scrape job details
            job = scraper.scrape_job_details(url)
            if not job:
                failed_jobs += 1
                continue
            
            # Create enhanced job data structure
            job_data = {
                'scenario': scenario['name'],
                'scenario_number': scenario_num,
                'job_index': j,
                'source': 'indeed',
                'title': job.title,
                'company': job.company,
                'location': job.location,
                'description': job.description[:1000] + "..." if len(job.description) > 1000 else job.description,
                'full_description_length': len(job.description),
                'salary': job.salary,
                'experience_level': job.experience_level,
                'job_type': job.job_type,
                'remote_option': job.remote_option,
                'url': job.url,
                'scraped_at': datetime.now().isoformat()
            }
            
            # Enhanced AI Analysis
            if ai_enabled:
                try:
                    analysis = ai_analyzer.analyze_job_comprehensive(
                        title=job.title,
                        company=job.company,
                        description=job.description,
                        location=job.location,
                        url=job.url
                    )
                    
                    # Comprehensive AI data extraction
                    job_data['ai_analysis'] = {
                        'confidence_score': analysis.confidence_score,
                        'analysis_quality': analysis.analysis_quality,
                        'openai_insights': {
                            'skills_required': analysis.openai_analysis.skills_required if analysis.openai_analysis else [],
                            'experience_level': analysis.openai_analysis.experience_level if analysis.openai_analysis else None,
                            'industry': analysis.openai_analysis.industry if analysis.openai_analysis else None,
                            'remote_friendly': analysis.openai_analysis.remote_friendly if analysis.openai_analysis else None,
                            'career_level': analysis.openai_analysis.career_level if analysis.openai_analysis else None
                        },
                        'claude_compensation': {
                            'salary_range': analysis.claude_compensation.salary_range if analysis.claude_compensation else None,
                            'benefits_mentioned': analysis.claude_compensation.benefits_mentioned if analysis.claude_compensation else [],
                            'compensation_score': analysis.claude_compensation.compensation_score if analysis.claude_compensation else None
                        },
                        'claude_requirements': {
                            'must_have_skills': analysis.claude_requirements.must_have_skills if analysis.claude_requirements else [],
                            'education_required': analysis.claude_requirements.education_required if analysis.claude_requirements else None,
                            'experience_required': analysis.claude_requirements.experience_required if analysis.claude_requirements else None
                        },
                        'analyzed_at': analysis.analyzed_at
                    }
                    
                    successful_jobs += 1
                    
                except Exception as e:
                    logger.debug(f"AI analysis failed for job {j}: {e}")
                    job_data['ai_analysis'] = {'error': str(e)}
                    failed_jobs += 1
            else:
                successful_jobs += 1
            
            scenario_results.append(job_data)
            
            # Rate limiting - be respectful to servers
            time.sleep(1)
            
        except Exception as e:
            logger.debug(f"Error processing job {j}: {e}")
            failed_jobs += 1
            continue
    
    logger.info(f"✅ Scenario processing complete: {successful_jobs} successful, {failed_jobs} failed")
    return scenario_results

def export_enhanced_results(results, processing_time):
    """Export enhanced results with comprehensive metadata."""
    
    try:
        results_dir = Path("data/results")
        results_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = results_dir / f"enhanced_analysis_{timestamp}.json"
        
        # Calculate comprehensive statistics
        total_jobs = len(results)
        ai_analyzed = sum(1 for job in results if 'ai_analysis' in job and 'error' not in job['ai_analysis'])
        
        # Extract detailed insights
        all_skills = []
        all_companies = []
        all_industries = []
        salary_data = []
        
        for job in results:
            if job.get('company'):
                all_companies.append(job['company'])
            
            if 'ai_analysis' in job and 'error' not in job['ai_analysis']:
                ai_data = job['ai_analysis']
                
                # Skills
                openai_skills = ai_data.get('openai_insights', {}).get('skills_required', [])
                claude_skills = ai_data.get('claude_requirements', {}).get('must_have_skills', [])
                all_skills.extend(openai_skills + claude_skills)
                
                # Industry
                industry = ai_data.get('openai_insights', {}).get('industry')
                if industry:
                    all_industries.append(industry)
                
                # Salary
                salary = ai_data.get('claude_compensation', {}).get('salary_range')
                if salary:
                    salary_data.append(salary)
        
        # Create comprehensive export
        export_data = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "analysis_type": "enhanced_large_scale",
                "total_jobs_collected": total_jobs,
                "processing_time_minutes": round(processing_time.total_seconds() / 60, 2),
                "ai_analysis_enabled": ai_analyzed > 0,
                "ai_success_rate": round((ai_analyzed / total_jobs) * 100, 1) if total_jobs > 0 else 0,
                "collection_period": "past_30_days"
            },
            "summary_statistics": {
                "total_jobs": total_jobs,
                "ai_analyzed_jobs": ai_analyzed,
                "unique_companies": len(set(all_companies)),
                "unique_skills_identified": len(set(all_skills)),
                "unique_industries": len(set(all_industries)),
                "jobs_with_salary_data": len(salary_data),
                "remote_jobs": sum(1 for job in results if job.get('remote_option'))
            },
            "jobs": results
        }
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Enhanced results exported to: {results_file}")
        logger.info(f"📊 Summary: {total_jobs} jobs, {ai_analyzed} with AI analysis ({(ai_analyzed/total_jobs)*100:.1f}%)")
        
        return results_file
        
    except Exception as e:
        logger.error(f"❌ Export failed: {e}")
        return None

def create_enhanced_dashboard(results_file):
    """Create enhanced analytical dashboard from results."""
    
    try:
        # Load results
        with open(results_file, 'r') as f:
            data = json.load(f)
        
        results = data.get('jobs', [])
        metadata = data.get('metadata', {})
        
        logger.info(f"📈 Creating dashboard for {len(results)} jobs...")
        
        # Generate analytics
        dashboard_data = {
            "overview": generate_overview_analytics(results, metadata),
            "skills_analysis": generate_skills_analytics(results),
            "company_analysis": generate_company_analytics(results),
            "location_analysis": generate_location_analytics(results),
            "salary_analysis": generate_salary_analytics(results),
            "industry_analysis": generate_industry_analytics(results)
        }
        
        # Export dashboard data
        dashboard_dir = Path("data/analytics")
        dashboard_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dashboard_file = dashboard_dir / f"dashboard_{timestamp}.json"
        
        with open(dashboard_file, 'w', encoding='utf-8') as f:
            json.dump(dashboard_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Analytics dashboard created: {dashboard_file}")
        
        # Display key insights
        display_key_insights(dashboard_data)
        
    except Exception as e:
        logger.error(f"❌ Dashboard creation failed: {e}")

def generate_overview_analytics(results, metadata):
    """Generate overview analytics."""
    
    total_jobs = len(results)
    return {
        "total_jobs_analyzed": total_jobs,
        "data_collection_time": metadata.get('processing_time_minutes', 0),
        "ai_analysis_coverage": metadata.get('ai_success_rate', 0),
        "remote_work_percentage": round((sum(1 for job in results if job.get('remote_option')) / total_jobs) * 100, 1) if total_jobs > 0 else 0,
        "data_quality_score": calculate_data_quality_score(results)
    }

def generate_skills_analytics(results):
    """Generate skills market analysis."""
    
    from collections import Counter
    
    all_skills = []
    for job in results:
        if 'ai_analysis' in job and 'error' not in job['ai_analysis']:
            ai_data = job['ai_analysis']
            openai_skills = ai_data.get('openai_insights', {}).get('skills_required', [])
            claude_skills = ai_data.get('claude_requirements', {}).get('must_have_skills', [])
            all_skills.extend(openai_skills + claude_skills)
    
    skill_counts = Counter(all_skills)
    top_skills = skill_counts.most_common(20)
    
    return {
        "total_skills_identified": len(set(all_skills)),
        "top_skills": [{"skill": skill, "count": count, "percentage": round((count/len(results))*100, 1)} 
                      for skill, count in top_skills],
        "skills_distribution": dict(skill_counts)
    }

def generate_company_analytics(results):
    """Generate company hiring analysis."""
    
    from collections import Counter
    
    companies = [job['company'] for job in results if job.get('company')]
    company_counts = Counter(companies)
    
    return {
        "total_companies": len(set(companies)),
        "top_hiring_companies": [{"company": company, "positions": count} 
                                for company, count in company_counts.most_common(15)],
        "hiring_diversity_score": calculate_hiring_diversity(company_counts)
    }

def generate_location_analytics(results):
    """Generate location and geographic analysis."""
    
    from collections import Counter
    
    locations = [job['location'] for job in results if job.get('location')]
    location_counts = Counter(locations)
    
    return {
        "total_locations": len(set(locations)),
        "top_job_markets": [{"location": location, "jobs": count} 
                           for location, count in location_counts.most_common(10)],
        "remote_jobs_count": sum(1 for job in results if job.get('remote_option')),
        "geographic_distribution": dict(location_counts)
    }

def generate_salary_analytics(results):
    """Generate salary and compensation analysis."""
    
    salary_data = []
    for job in results:
        # Direct salary data
        if job.get('salary'):
            salary_data.append(job['salary'])
        
        # AI-extracted salary data
        if 'ai_analysis' in job and 'error' not in job['ai_analysis']:
            ai_salary = job['ai_analysis'].get('claude_compensation', {}).get('salary_range')
            if ai_salary:
                salary_data.append(ai_salary)
    
    return {
        "jobs_with_salary_data": len(salary_data),
        "salary_coverage_percentage": round((len(salary_data) / len(results)) * 100, 1),
        "salary_ranges": salary_data,
        "sample_salaries": salary_data[:10]  # Show first 10 as examples
    }

def generate_industry_analytics(results):
    """Generate industry distribution analysis."""
    
    from collections import Counter
    
    industries = []
    for job in results:
        if 'ai_analysis' in job and 'error' not in job['ai_analysis']:
            industry = job['ai_analysis'].get('openai_insights', {}).get('industry')
            if industry:
                industries.append(industry)
    
    industry_counts = Counter(industries)
    
    return {
        "total_industries": len(set(industries)),
        "industry_distribution": [{"industry": industry, "jobs": count, "percentage": round((count/len(industries))*100, 1)} 
                                 for industry, count in industry_counts.most_common()],
        "industry_diversity_score": len(set(industries))
    }

def calculate_data_quality_score(results):
    """Calculate overall data quality score."""
    
    total_jobs = len(results)
    if total_jobs == 0:
        return 0
    
    # Quality factors
    has_title = sum(1 for job in results if job.get('title'))
    has_company = sum(1 for job in results if job.get('company'))
    has_description = sum(1 for job in results if job.get('description'))
    has_ai_analysis = sum(1 for job in results if 'ai_analysis' in job and 'error' not in job['ai_analysis'])
    
    quality_score = (
        (has_title / total_jobs) * 0.2 +
        (has_company / total_jobs) * 0.2 +
        (has_description / total_jobs) * 0.3 +
        (has_ai_analysis / total_jobs) * 0.3
    ) * 100
    
    return round(quality_score, 1)

def calculate_hiring_diversity(company_counts):
    """Calculate hiring diversity score."""
    
    total_companies = len(company_counts)
    if total_companies == 0:
        return 0
    
    # Higher score = more diverse hiring (companies hire similar numbers)
    # Lower score = concentrated hiring (few companies hire many)
    total_jobs = sum(company_counts.values())
    avg_jobs_per_company = total_jobs / total_companies
    
    # Companies hiring close to average get higher diversity score
    diversity_score = min(100, (1 / (1 + abs(max(company_counts.values()) - avg_jobs_per_company) / avg_jobs_per_company)) * 100)
    
    return round(diversity_score, 1)

def display_key_insights(dashboard_data):
    """Display key insights from the dashboard."""
    
    logger.info("\n🎯 Key Market Insights")
    logger.info("=" * 30)
    
    overview = dashboard_data.get('overview', {})
    skills = dashboard_data.get('skills_analysis', {})
    companies = dashboard_data.get('company_analysis', {})
    locations = dashboard_data.get('location_analysis', {})
    
    # Overview insights
    logger.info(f"📊 Jobs Analyzed: {overview.get('total_jobs_analyzed', 0)}")
    logger.info(f"🤖 AI Analysis Coverage: {overview.get('ai_analysis_coverage', 0)}%")
    logger.info(f"🏠 Remote Work Availability: {overview.get('remote_work_percentage', 0)}%")
    logger.info(f"⭐ Data Quality Score: {overview.get('data_quality_score', 0)}/100")
    
    # Top skills
    top_skills = skills.get('top_skills', [])[:5]
    if top_skills:
        logger.info("\n🛠️ Top 5 In-Demand Skills:")
        for i, skill_data in enumerate(top_skills, 1):
            logger.info(f"  {i}. {skill_data['skill']}: {skill_data['count']} jobs ({skill_data['percentage']}%)")
    
    # Top companies
    top_companies = companies.get('top_hiring_companies', [])[:5]
    if top_companies:
        logger.info("\n🏢 Top 5 Hiring Companies:")
        for i, company_data in enumerate(top_companies, 1):
            logger.info(f"  {i}. {company_data['company']}: {company_data['positions']} positions")
    
    # Top locations
    top_locations = locations.get('top_job_markets', [])[:5]
    if top_locations:
        logger.info("\n📍 Top 5 Job Markets:")
        for i, location_data in enumerate(top_locations, 1):
            logger.info(f"  {i}. {location_data['location']}: {location_data['jobs']} jobs")
    
    logger.info("\n🎉 Enhanced analysis complete! Dashboard data ready for visualization.")

if __name__ == "__main__":
    try:
        enhanced_job_analysis()
    except KeyboardInterrupt:
        logger.info("\n⚠️ Analysis interrupted by user")
    except Exception as e:
        logger.error(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
