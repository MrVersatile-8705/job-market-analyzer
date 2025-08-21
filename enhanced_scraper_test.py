#!/usr/bin/env python3
"""
Multi-Scraper Test with Optional AI Integration

This script tests enhanced scrapers and demonstrates AI integration capabilities.
Works with or without AI API keys - provides graceful degradation.
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

# Try to import AI components
try:
    from src.ai_analysis.job_analyzer import AIJobAnalyzer
    AI_AVAILABLE = True
except ImportError as e:
    logger.warning(f"AI components not available: {e}")
    AI_AVAILABLE = False

# Configure logging
logger.remove()
logger.add(
    "logs/multi_scraper_test.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="INFO",
    rotation="10 MB"
)
logger.add(sys.stdout, level="INFO")

def test_enhanced_scrapers():
    """Test enhanced scraping capabilities with optional AI analysis."""
    
    logger.info("🚀 Starting Enhanced Job Market Analysis")
    logger.info("=" * 60)
    
    # Check AI availability
    if AI_AVAILABLE:
        logger.info("🤖 AI Analysis: ENABLED")
        ai_analyzer = AIJobAnalyzer()
    else:
        logger.info("🤖 AI Analysis: DISABLED (API keys not configured)")
        ai_analyzer = None
    
    # Initialize scrapers
    settings = Settings()
    indeed_scraper = IndeedScraper()
    
    # Test scenarios for different scrapers
    test_scenarios = [
        {
            "name": "Data Analyst Remote Jobs",
            "scraper": "indeed",
            "keywords": ["Data Analyst", "Remote"],
            "location": "",
            "limit": 5
        },
        {
            "name": "Senior Data Scientists - Bay Area",
            "scraper": "indeed", 
            "keywords": ["Senior Data Scientist"],
            "location": "San Francisco, CA",
            "limit": 3
        },
        {
            "name": "Business Intelligence - NYC",
            "scraper": "indeed",
            "keywords": ["Business Intelligence", "SQL"],
            "location": "New York, NY", 
            "limit": 3
        }
    ]
    
    all_results = []
    
    for i, scenario in enumerate(test_scenarios, 1):
        logger.info(f"\n📊 Scenario {i}: {scenario['name']}")
        logger.info("-" * 50)
        
        try:
            # Step 1: Job Search
            logger.info(f"🔍 Searching for: {', '.join(scenario['keywords'])}")
            
            if scenario['scraper'] == 'indeed':
                job_urls = indeed_scraper.search_jobs(
                    keywords=scenario['keywords'],
                    location=scenario['location'],
                    limit=scenario['limit']
                )
            else:
                logger.warning(f"Scraper {scenario['scraper']} not implemented yet")
                continue
            
            if not job_urls:
                logger.warning(f"No jobs found for scenario {i}")
                continue
                
            logger.info(f"✅ Found {len(job_urls)} job URLs")
            
            # Step 2: Detailed Scraping
            logger.info("📄 Extracting job details...")
            scenario_jobs = []
            
            for j, url in enumerate(job_urls[:scenario['limit']], 1):
                logger.info(f"  Processing job {j}/{len(job_urls[:scenario['limit']])}")
                
                try:
                    job = indeed_scraper.scrape_job_details(url)
                    if job:
                        job_data = {
                            'scenario': scenario['name'],
                            'source': 'indeed',
                            'title': job.title,
                            'company': job.company,
                            'location': job.location,
                            'description': job.description,
                            'salary': job.salary,
                            'experience_level': job.experience_level,
                            'job_type': job.job_type,
                            'remote_option': job.remote_option,
                            'url': job.url,
                            'scraped_at': datetime.now().isoformat()
                        }
                        
                        # Step 3: Optional AI Analysis
                        if ai_analyzer:
                            logger.info(f"    🤖 Running AI analysis...")
                            try:
                                ai_analysis = ai_analyzer.analyze_job_comprehensive(
                                    title=job.title,
                                    company=job.company,
                                    description=job.description,
                                    location=job.location,
                                    url=job.url
                                )
                                
                                job_data['ai_analysis'] = {
                                    'confidence_score': ai_analysis.confidence_score,
                                    'analysis_quality': ai_analysis.analysis_quality,
                                    'skills_required': ai_analysis.openai_analysis.skills_required if ai_analysis.openai_analysis else [],
                                    'experience_level_ai': ai_analysis.openai_analysis.experience_level if ai_analysis.openai_analysis else None,
                                    'industry': ai_analysis.openai_analysis.industry if ai_analysis.openai_analysis else None,
                                    'remote_friendly': ai_analysis.openai_analysis.remote_friendly if ai_analysis.openai_analysis else None,
                                    'salary_estimate': ai_analysis.claude_compensation.salary_range if ai_analysis.claude_compensation else None,
                                    'key_highlights': ai_analysis.combined_insights.get('key_highlights', []),
                                    'opportunity_rating': ai_analysis.combined_insights.get('opportunity_rating', 'unknown'),
                                    'analyzed_at': ai_analysis.analyzed_at
                                }
                                
                                logger.info(f"    ✅ AI analysis complete (Quality: {ai_analysis.analysis_quality})")
                                
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
    
    # Summary Analysis
    logger.info(f"\n📈 Analysis Summary")
    logger.info("=" * 40)
    
    if all_results:
        total_jobs = len(all_results)
        logger.info(f"📊 Total Jobs Analyzed: {total_jobs}")
        
        # Source distribution
        source_counts = {}
        for job in all_results:
            source = job['source']
            source_counts[source] = source_counts.get(source, 0) + 1
        
        logger.info("🔗 Source Distribution:")
        for source, count in source_counts.items():
            logger.info(f"  {source.title()}: {count}")
        
        # Remote work analysis
        remote_jobs = sum(1 for job in all_results if job.get('remote_option'))
        remote_percentage = (remote_jobs / total_jobs) * 100
        logger.info(f"🏠 Remote Work: {remote_jobs}/{total_jobs} ({remote_percentage:.1f}%)")
        
        # Company analysis
        companies = set(job['company'] for job in all_results if job['company'])
        logger.info(f"🏢 Unique Companies: {len(companies)}")
        
        # AI Analysis Summary
        if ai_analyzer:
            ai_analyzed = sum(1 for job in all_results if 'ai_analysis' in job and 'error' not in job['ai_analysis'])
            ai_percentage = (ai_analyzed / total_jobs) * 100
            logger.info(f"🤖 AI Analysis: {ai_analyzed}/{total_jobs} ({ai_percentage:.1f}%)")
            
            if ai_analyzed > 0:
                # Quality distribution
                quality_counts = {}
                confidence_scores = []
                
                for job in all_results:
                    if 'ai_analysis' in job and 'error' not in job['ai_analysis']:
                        quality = job['ai_analysis'].get('analysis_quality', 'unknown')
                        quality_counts[quality] = quality_counts.get(quality, 0) + 1
                        
                        confidence = job['ai_analysis'].get('confidence_score', 0)
                        confidence_scores.append(confidence)
                
                logger.info("⭐ AI Analysis Quality:")
                for quality, count in quality_counts.items():
                    logger.info(f"  {quality.title()}: {count}")
                
                if confidence_scores:
                    avg_confidence = sum(confidence_scores) / len(confidence_scores)
                    logger.info(f"🎯 Average Confidence: {avg_confidence:.2%}")
        
        # Skills analysis (basic)
        logger.info("\n🛠️ Top Skills Mentioned:")
        skill_keywords = ['python', 'sql', 'tableau', 'excel', 'r', 'powerbi', 'aws', 'machine learning', 'statistics']
        skill_counts = {}
        
        for job in all_results:
            description = job.get('description', '').lower()
            for skill in skill_keywords:
                if skill in description:
                    skill_counts[skill] = skill_counts.get(skill, 0) + 1
        
        # Show top skills
        sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)
        for skill, count in sorted_skills[:8]:
            percentage = (count / total_jobs) * 100
            logger.info(f"  {skill.title()}: {count} ({percentage:.1f}%)")
    
    # Export Results
    logger.info(f"\n💾 Exporting Results")
    logger.info("-" * 30)
    
    try:
        # Ensure results directory exists
        results_dir = Path("data/results")
        results_dir.mkdir(parents=True, exist_ok=True)
        
        # Export detailed results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = results_dir / f"enhanced_scraper_test_{timestamp}.json"
        
        export_data = {
            "test_metadata": {
                "timestamp": datetime.now().isoformat(),
                "total_jobs": len(all_results),
                "scenarios_tested": len(test_scenarios),
                "ai_analysis_enabled": ai_analyzer is not None,
                "scrapers_tested": ["indeed"]
            },
            "jobs": all_results,
            "summary_stats": {
                "total_jobs": len(all_results),
                "source_distribution": source_counts if 'source_counts' in locals() else {},
                "remote_percentage": remote_percentage if 'remote_percentage' in locals() else 0,
                "unique_companies": len(companies) if 'companies' in locals() else 0
            }
        }
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Results exported to: {results_file}")
        
    except Exception as e:
        logger.error(f"❌ Export failed: {e}")
    
    # Next Steps
    logger.info(f"\n🎯 Next Steps")
    logger.info("-" * 20)
    
    if not AI_AVAILABLE:
        logger.info("1. 🔑 Configure AI API keys in .env file:")
        logger.info("   OPENAI_API_KEY=your_openai_key_here")
        logger.info("   CLAUDE_API_KEY=your_claude_key_here")
        logger.info("2. 📦 Install AI dependencies:")
        logger.info("   pip install openai anthropic")
    
    logger.info("3. 🔧 Add more scrapers:")
    logger.info("   - LinkedIn scraper (when ready)")
    logger.info("   - Glassdoor scraper (when ready)")
    
    logger.info("4. 📊 Build data visualization:")
    logger.info("   - Interactive dashboards")
    logger.info("   - Trend analysis")
    logger.info("   - Market insights")
    
    logger.info(f"\n🎉 Test Complete!")
    logger.info(f"Successfully processed {len(all_results)} jobs from {len(test_scenarios)} scenarios")

if __name__ == "__main__":
    test_enhanced_scrapers()
