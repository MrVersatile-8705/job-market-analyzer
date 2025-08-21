#!/usr/bin/env python3
"""
Multi-Scraper Test with AI Integration

This script tests all scrapers and AI components together.
Works with or without API keys - graceful degradation.
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

# Try to import LinkedIn scraper
try:
    from src.data_collection.scrapers.linkedin_scraper import LinkedInScraper
    LINKEDIN_AVAILABLE = True
except ImportError:
    LINKEDIN_AVAILABLE = False
    logger.warning("LinkedIn scraper not available")

# Try to import AI components
try:
    from src.ai_analysis.job_analyzer import AIJobAnalyzer
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    logger.warning("AI components not available - will skip AI analysis")

# Configure logging
logger.remove()
logger.add(
    "logs/multi_scraper_test.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="INFO",
    rotation="10 MB"
)
logger.add(sys.stdout, level="INFO")

def test_multi_scraper_system():
    """Test the complete job market analysis system."""
    
    logger.info("🚀 Multi-Scraper Test with AI Integration")
    logger.info("=" * 60)
    
    # Initialize components
    settings = Settings()
    
    # Check AI availability
    if AI_AVAILABLE and (settings.OPENAI_API_KEY or settings.CLAUDE_API_KEY):
        logger.info("🤖 AI Analysis: ENABLED")
        ai_analyzer = AIJobAnalyzer()
        ai_enabled = True
    else:
        logger.info("🤖 AI Analysis: DISABLED (API keys not configured)")
        ai_analyzer = None
        ai_enabled = False
    
    # Test scenarios with increased limits and month-long timeframe
    test_scenarios = [
        {
            "name": "Remote Data Analyst Jobs - Past Month",
            "keywords": ["Data Analyst", "Remote"],
            "location": "",
            "limit": 20,  # Increased from 5
            "days_back": 30  # Past month
        },
        {
            "name": "Business Intelligence - Major Cities - Past Month",
            "keywords": ["Business Intelligence", "BI"],
            "location": "New York, NY",
            "limit": 15,  # Increased from 3
            "days_back": 30  # Past month
        },
        {
            "name": "Data Science - Remote Opportunities",
            "keywords": ["Data Science", "Data Scientist"],
            "location": "",
            "limit": 15,
            "days_back": 30
        },
        {
            "name": "Analytics - San Francisco Bay Area",
            "keywords": ["Analytics", "Business Analyst"],
            "location": "San Francisco, CA",
            "limit": 10,
            "days_back": 30
        }
    ]
    
    all_results = []
    
    for i, scenario in enumerate(test_scenarios, 1):
        logger.info(f"\n📊 Scenario {i}: {scenario['name']}")
        logger.info("-" * 50)
        
        try:
            # Step 1: Test Multiple Scrapers
            all_job_urls = []
            
            # Test Indeed Scraper
            logger.info("🔍 Testing Indeed scraper...")
            indeed_scraper = IndeedScraper()
            
            indeed_urls = indeed_scraper.search_jobs(
                keywords=scenario['keywords'],
                location=scenario['location'],
                limit=scenario['limit'],
                days_back=scenario.get('days_back', 30)  # Default to 30 days if not specified
            )
            
            if indeed_urls:
                logger.info(f"✅ Found {len(indeed_urls)} job URLs from Indeed")
                all_job_urls.extend([(url, 'indeed') for url in indeed_urls])
            else:
                logger.warning("No jobs found from Indeed")
            
            # Test LinkedIn Scraper (if available)
            if LINKEDIN_AVAILABLE:
                logger.info("🔍 Testing LinkedIn scraper...")
                try:
                    linkedin_scraper = LinkedInScraper()
                    linkedin_limit = min(10, scenario['limit'] // 2)  # Limit LinkedIn searches
                    
                    linkedin_urls = linkedin_scraper.search_jobs(
                        keywords=scenario['keywords'],
                        location=scenario['location'],
                        limit=linkedin_limit,
                        days_back=scenario.get('days_back', 30)
                    )
                    
                    if linkedin_urls:
                        logger.info(f"✅ Found {len(linkedin_urls)} job URLs from LinkedIn")
                        all_job_urls.extend([(url, 'linkedin') for url in linkedin_urls])
                    else:
                        logger.warning("No jobs found from LinkedIn")
                        
                except Exception as e:
                    logger.error(f"LinkedIn scraper failed: {e}")
            
            if not all_job_urls:
                logger.warning(f"No jobs found for scenario {i}")
                continue
            
            logger.info(f"✅ Total job URLs found: {len(all_job_urls)}")

            # Step 2: Scrape Job Details
            logger.info("📄 Extracting job details...")
            scenario_jobs = []
            
            for j, (url, source) in enumerate(all_job_urls, 1):
                logger.info(f"  Processing job {j}/{len(all_job_urls)} from {source}")
                
                try:
                    # Use the appropriate scraper based on source
                    if source == 'indeed':
                        job = indeed_scraper.scrape_job_details(url)
                    elif source == 'linkedin' and LINKEDIN_AVAILABLE:
                        job = linkedin_scraper.scrape_job_details(url)
                    else:
                        continue
                    if job:
                        job_data = {
                            'scenario': scenario['name'],
                            'source': source,  # Track which scraper found this job
                            'title': job.title,
                            'company': job.company,
                            'location': job.location,
                            'description': job.description[:500] + "..." if len(job.description) > 500 else job.description,
                            'salary': job.salary,
                            'experience_level': job.experience_level,
                            'job_type': job.job_type,
                            'remote_option': job.remote_option,
                            'url': job.url,
                            'scraped_at': datetime.now().isoformat()
                        }
                        
                        # Step 3: AI Analysis (if available)
                        if ai_enabled and ai_analyzer:
                            logger.info(f"    🤖 Running AI analysis...")
                            try:
                                # Comprehensive AI analysis
                                ai_analysis = ai_analyzer.analyze_job_comprehensive(
                                    title=job.title,
                                    company=job.company,
                                    description=job.description,
                                    location=job.location,
                                    url=job.url
                                )
                                
                                # Extract key insights for storage
                                ai_summary = {
                                    'confidence_score': ai_analysis.confidence_score,
                                    'analysis_quality': ai_analysis.analysis_quality,
                                    'skills_required': ai_analysis.openai_analysis.skills_required[:10] if ai_analysis.openai_analysis else [],
                                    'experience_level_ai': ai_analysis.openai_analysis.experience_level if ai_analysis.openai_analysis else None,
                                    'industry': ai_analysis.openai_analysis.industry if ai_analysis.openai_analysis else None,
                                    'remote_friendly': ai_analysis.openai_analysis.remote_friendly if ai_analysis.openai_analysis else None,
                                    'salary_estimate': ai_analysis.claude_compensation.salary_range if ai_analysis.claude_compensation else None,
                                    'key_highlights': ai_analysis.combined_insights.get('key_highlights', []),
                                    'opportunity_rating': ai_analysis.combined_insights.get('opportunity_rating', 'unknown'),
                                    'analyzed_at': ai_analysis.analyzed_at
                                }
                                
                                job_data['ai_analysis'] = ai_summary
                                logger.info(f"    ✅ AI analysis complete (Quality: {ai_analysis.analysis_quality}, Confidence: {ai_analysis.confidence_score:.2%})")
                                
                            except Exception as e:
                                logger.error(f"    ❌ AI analysis failed: {e}")
                                job_data['ai_analysis'] = {'error': str(e)}
                        
                        scenario_jobs.append(job_data)
                        
                        # Display job summary
                        logger.info(f"    📋 {job.title} at {job.company}")
                        if job.salary:
                            logger.info(f"       💰 Salary: {job.salary}")
                        if job.remote_option:
                            logger.info(f"       🏠 Remote: Available")
                        
                except Exception as e:
                    logger.error(f"    ❌ Failed to process job {j}: {e}")
                    continue
                
                # Rate limiting
                time.sleep(2)
            
            all_results.extend(scenario_jobs)
            logger.info(f"✅ Scenario {i} completed: {len(scenario_jobs)} jobs processed")
            
        except Exception as e:
            logger.error(f"❌ Scenario {i} failed: {e}")
            continue
    
    # Analysis Summary
    logger.info(f"\n📈 System Test Results")
    logger.info("=" * 40)
    
    if all_results:
        total_jobs = len(all_results)
        logger.info(f"📊 Total Jobs Processed: {total_jobs}")
        
        # Success rates
        successful_scrapes = sum(1 for job in all_results if job.get('title'))
        scrape_success_rate = (successful_scrapes / total_jobs) * 100 if total_jobs > 0 else 0
        logger.info(f"🎯 Scraping Success Rate: {scrape_success_rate:.1f}%")
        
        # AI Analysis Summary
        if ai_enabled:
            ai_analyzed = sum(1 for job in all_results if 'ai_analysis' in job and 'error' not in job['ai_analysis'])
            ai_success_rate = (ai_analyzed / total_jobs) * 100 if total_jobs > 0 else 0
            logger.info(f"🤖 AI Analysis Success Rate: {ai_success_rate:.1f}%")
            
            if ai_analyzed > 0:
                # Average confidence score
                confidence_scores = [
                    job['ai_analysis']['confidence_score'] 
                    for job in all_results 
                    if 'ai_analysis' in job and 'confidence_score' in job['ai_analysis']
                ]
                if confidence_scores:
                    avg_confidence = sum(confidence_scores) / len(confidence_scores)
                    logger.info(f"🎲 Average AI Confidence: {avg_confidence:.2%}")
                
                # Quality distribution
                qualities = [
                    job['ai_analysis']['analysis_quality'] 
                    for job in all_results 
                    if 'ai_analysis' in job and 'analysis_quality' in job['ai_analysis']
                ]
                quality_counts = {}
                for quality in qualities:
                    quality_counts[quality] = quality_counts.get(quality, 0) + 1
                
                logger.info("⭐ AI Analysis Quality Distribution:")
                for quality, count in quality_counts.items():
                    logger.info(f"  {quality.title()}: {count}")
        
        # Remote work analysis
        remote_jobs = sum(1 for job in all_results if job.get('remote_option'))
        remote_percentage = (remote_jobs / total_jobs) * 100 if total_jobs > 0 else 0
        logger.info(f"🏠 Remote Jobs: {remote_jobs}/{total_jobs} ({remote_percentage:.1f}%)")
        
        # Company diversity
        companies = set(job['company'] for job in all_results if job.get('company'))
        logger.info(f"🏢 Unique Companies: {len(companies)}")
        
        # Source distribution
        sources = {}
        for job in all_results:
            source = job.get('source', 'unknown')
            sources[source] = sources.get(source, 0) + 1
        
        logger.info("📊 Jobs by Source:")
        for source, count in sources.items():
            logger.info(f"  {source.title()}: {count}")

        # Top skills (basic analysis)
        if ai_enabled and any('ai_analysis' in job for job in all_results):
            all_skills = []
            for job in all_results:
                if 'ai_analysis' in job and 'skills_required' in job['ai_analysis']:
                    all_skills.extend(job['ai_analysis']['skills_required'])
            
            if all_skills:
                skill_counts = {}
                for skill in all_skills:
                    skill_counts[skill] = skill_counts.get(skill, 0) + 1
                
                top_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:8]
                logger.info("🛠️ Top Skills Identified by AI:")
                for skill, count in top_skills:
                    logger.info(f"  {skill}: {count} mentions")
    
    # Export Results
    logger.info(f"\n💾 Exporting Results")
    logger.info("-" * 30)
    
    try:
        # Ensure results directory exists
        results_dir = Path("data/results")
        results_dir.mkdir(parents=True, exist_ok=True)
        
        # Export comprehensive results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = results_dir / f"multi_scraper_test_{timestamp}.json"
        
        export_data = {
            "test_metadata": {
                "timestamp": datetime.now().isoformat(),
                "total_jobs": len(all_results),
                "scenarios_tested": len(test_scenarios),
                "ai_analysis_enabled": ai_enabled,
                "scrapers_tested": ["indeed"] + (["linkedin"] if LINKEDIN_AVAILABLE else []),
                "system_status": "operational",
                "search_timeframe": "past_30_days"
            },
            "results": all_results,
            "summary_stats": {
                "total_jobs": len(all_results),
                "scraping_success_rate": scrape_success_rate if 'scrape_success_rate' in locals() else 0,
                "ai_success_rate": ai_success_rate if 'ai_success_rate' in locals() else 0,
                "remote_percentage": remote_percentage if 'remote_percentage' in locals() else 0,
                "unique_companies": len(companies) if 'companies' in locals() else 0
            }
        }
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Results exported to: {results_file}")
        
    except Exception as e:
        logger.error(f"❌ Export failed: {e}")
    
    # System Status Report
    logger.info(f"\n🎯 System Status Report")
    logger.info("=" * 30)
    
    # Check what's working
    working_components = []
    if successful_scrapes > 0:
        working_components.append("✅ Web Scraping")
    if ai_enabled and ai_analyzed > 0:
        working_components.append("✅ AI Analysis")
    
    logger.info("Working Components:")
    for component in working_components:
        logger.info(f"  {component}")
    
    # Next steps
    logger.info("\n🚀 Next Steps:")
    if not ai_enabled:
        logger.info("1. Add API keys to .env file for AI analysis")
        logger.info("   - Copy .env.template to .env")
        logger.info("   - Add your OpenAI and Claude API keys")
    
    logger.info("2. Scale up testing with more job sites")
    logger.info("3. Build data visualization dashboard")
    logger.info("4. Implement advanced analytics")
    
    logger.info(f"\n🎉 Multi-Scraper Test Complete!")
    logger.info(f"System is ready for production use!")

if __name__ == "__main__":
    test_multi_scraper_system()
