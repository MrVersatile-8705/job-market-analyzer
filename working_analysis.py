#!/usr/bin/env python3
"""
Working Large-Scale Job Market Analysis
Uses proven keywords and approaches from successful tests
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
from src.data_collection.scrapers.indeed_scraper import IndeedScraper
from src.ai_analysis.job_analyzer import AIJobAnalyzer

# Configure logging
logger.remove()
logger.add(
    "logs/working_analysis.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="INFO",
    rotation="10 MB"
)
logger.add(sys.stdout, level="INFO")

def working_job_analysis():
    """Run working job market analysis using proven keywords."""
    
    logger.info("🚀 Working Large-Scale Job Market Analysis")
    logger.info("Using proven keywords from successful tests")
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
    
    # Define working test scenarios using proven keywords
    test_scenarios = [
        {
            "name": "Data Analyst - Cleveland Market",
            "keywords": ["Data Analyst"],
            "location": "Cleveland, OH",
            "limit": 25,
            "days_back": 30,
        },
        {
            "name": "Data Analyst - New York Market",
            "keywords": ["Data Analyst"],
            "location": "New York, NY",
            "limit": 25,
            "days_back": 30,
        },
        {
            "name": "Data Analyst - Remote Positions",
            "keywords": ["Data Analyst"],
            "location": "Remote",
            "limit": 25,
            "days_back": 30,
        },
        {
            "name": "Business Analyst - National Search",
            "keywords": ["Business Analyst"],
            "location": "",
            "limit": 25,
            "days_back": 30,
        }
    ]
    
    total_target = sum(scenario['limit'] for scenario in test_scenarios)
    logger.info(f"📊 Target: {total_target} jobs across {len(test_scenarios)} scenarios")
    logger.info("⏱️ Estimated time: 60-90 minutes")
    
    # Confirm before proceeding
    proceed = input(f"\nProceed with working analysis ({total_target} jobs)? (y/n): ")
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
            scenario_results = process_working_scenario(scenario, ai_analyzer, ai_enabled, i)
            all_results.extend(scenario_results)
            
            # Progress update
            logger.info(f"✅ Scenario {i} completed: {len(scenario_results)} jobs | Total: {len(all_results)}")
            
            # Break if we have enough data
            if len(all_results) >= 50:
                logger.info(f"🎯 Reached sufficient data collection: {len(all_results)} jobs")
                break
                
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
    
    logger.info(f"\n🎉 Working Analysis Complete!")
    logger.info(f"⏱️ Total processing time: {processing_time}")
    logger.info(f"📊 Total jobs collected: {len(all_results)}")
    
    # Export results and create analytics
    if all_results:
        results_file = export_working_results(all_results, processing_time)
        
        if results_file:
            logger.info("\n📈 Creating analytical dashboard...")
            create_working_dashboard(results_file)
    else:
        logger.warning("❌ No jobs collected. Check network connection and scraper configuration.")

def process_working_scenario(scenario, ai_analyzer, ai_enabled, scenario_num):
    """Process a single scenario with working approach."""
    
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
        
        # Try alternative search with broader keywords
        logger.info("🔄 Trying broader search...")
        if "Data Analyst" in scenario['keywords']:
            alternative_keywords = ["analyst"]
            job_urls = scraper.search_jobs(
                keywords=alternative_keywords,
                location=scenario['location'],
                limit=min(15, scenario['limit']),
                days_back=scenario.get('days_back', 30)
            )
        
        if not job_urls:
            logger.warning(f"No jobs found even with broader search")
            return []
    
    logger.info(f"✅ Found {len(job_urls)} job URLs")
    
    # Process jobs with enhanced tracking
    scenario_results = []
    successful_jobs = 0
    failed_jobs = 0
    
    for j, url in enumerate(job_urls, 1):
        try:
            # Progress indicator
            if j % 5 == 0 or j == len(job_urls):
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
            time.sleep(2)
            
        except Exception as e:
            logger.debug(f"Error processing job {j}: {e}")
            failed_jobs += 1
            continue
    
    logger.info(f"✅ Scenario processing complete: {successful_jobs} successful, {failed_jobs} failed")
    return scenario_results

def export_working_results(results, processing_time):
    """Export working results with comprehensive metadata."""
    
    try:
        results_dir = Path("data/results")
        results_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = results_dir / f"working_analysis_{timestamp}.json"
        
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
                "analysis_type": "working_large_scale",
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
        
        logger.info(f"✅ Working results exported to: {results_file}")
        logger.info(f"📊 Summary: {total_jobs} jobs, {ai_analyzed} with AI analysis ({(ai_analyzed/total_jobs)*100:.1f}%)")
        
        return results_file
        
    except Exception as e:
        logger.error(f"❌ Export failed: {e}")
        return None

def create_working_dashboard(results_file):
    """Create working analytical dashboard from results."""
    
    try:
        logger.info("📈 Running advanced analytics dashboard...")
        
        # Run the advanced analytics module
        import subprocess
        result = subprocess.run([
            sys.executable, "advanced_analytics.py", str(results_file)
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            logger.info("✅ Advanced analytics dashboard created successfully")
            logger.info(result.stdout)
        else:
            logger.error(f"❌ Dashboard creation failed: {result.stderr}")
            
    except Exception as e:
        logger.error(f"❌ Dashboard creation failed: {e}")

if __name__ == "__main__":
    try:
        working_job_analysis()
    except KeyboardInterrupt:
        logger.info("\n⚠️ Analysis interrupted by user")
    except Exception as e:
        logger.error(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
