#!/usr/bin/env python3
"""
Advanced Job Market Analysis with Multiple Scrapers + AI Integration

This script demonstrates the enhanced job market analysis system with:
- Multiple job site scrapers (Indeed, LinkedIn, Glassdoor)
- AI-powered analysis using OpenAI and Claude
- Comprehensive data processing and insights
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
    "logs/ai_enhanced_test.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="INFO",
    rotation="10 MB"
)
logger.add(sys.stdout, level="INFO")

def test_multi_scraper_with_ai():
    """Test multiple scrapers with AI analysis integration."""
    
    logger.info("🚀 Starting Advanced Job Market Analysis")
    logger.info("=" * 60)
    
    # Initialize components
    settings = Settings()
    indeed_scraper = IndeedScraper()
    ai_analyzer = AIJobAnalyzer()
    
    # Test scenarios
    test_cases = [
        {
            "name": "Senior Data Scientist - Tech Hubs",
            "keywords": ["Senior Data Scientist", "Machine Learning"],
            "location": "San Francisco, CA",
            "limit": 3
        },
        {
            "name": "Data Analyst - Remote Opportunities", 
            "keywords": ["Data Analyst", "Remote"],
            "location": "",  # No location for remote search
            "limit": 3
        },
        {
            "name": "Business Intelligence - Financial Services",
            "keywords": ["Business Intelligence", "SQL", "Tableau"],
            "location": "New York, NY",
            "limit": 2
        }
    ]
    
    all_analyses = []
    
    for i, test_case in enumerate(test_cases, 1):
        logger.info(f"\n📊 Test Case {i}: {test_case['name']}")
        logger.info("-" * 50)
        
        try:
            # Step 1: Search for jobs
            logger.info(f"🔍 Searching Indeed for: {', '.join(test_case['keywords'])}")
            job_urls = indeed_scraper.search_jobs(
                keywords=test_case['keywords'],
                location=test_case['location'],
                limit=test_case['limit']
            )
            
            if not job_urls:
                logger.warning(f"No jobs found for test case {i}")
                continue
            
            logger.info(f"✅ Found {len(job_urls)} job URLs")
            
            # Step 2: Scrape detailed job information
            logger.info("📄 Scraping job details...")
            jobs = []
            
            for j, url in enumerate(job_urls, 1):
                logger.info(f"  Scraping job {j}/{len(job_urls)}")
                
                job = indeed_scraper.scrape_job_details(url)
                if job:
                    jobs.append({
                        'title': job.title,
                        'company': job.company,
                        'location': job.location,
                        'description': job.description,
                        'salary': job.salary,
                        'url': job.url,
                        'remote_option': job.remote_option,
                        'job_type': job.job_type,
                        'experience_level': job.experience_level
                    })
                
                # Rate limiting
                time.sleep(2)
            
            logger.info(f"✅ Successfully scraped {len(jobs)} job details")
            
            # Step 3: AI Analysis
            logger.info("🤖 Performing AI analysis...")
            
            for k, job in enumerate(jobs, 1):
                logger.info(f"  Analyzing job {k}/{len(jobs)}: {job['title']}")
                
                try:
                    # Comprehensive AI analysis
                    analysis = ai_analyzer.analyze_job_comprehensive(
                        title=job['title'],
                        company=job['company'],
                        description=job['description'],
                        location=job['location'],
                        url=job['url']
                    )
                    
                    # Add scraped data to analysis
                    analysis_dict = {
                        'test_case': test_case['name'],
                        'scraped_data': job,
                        'ai_analysis': analysis,
                        'analysis_summary': ai_analyzer.get_analysis_summary(analysis)
                    }
                    
                    all_analyses.append(analysis_dict)
                    
                    # Display immediate summary
                    logger.info(f"📋 Analysis Summary for {job['title']}:")
                    summary_lines = ai_analyzer.get_analysis_summary(analysis).split('\n')
                    for line in summary_lines:
                        logger.info(f"    {line}")
                    
                except Exception as e:
                    logger.error(f"❌ AI analysis failed for {job['title']}: {e}")
                    continue
            
            logger.info(f"✅ Completed AI analysis for test case {i}")
            
        except Exception as e:
            logger.error(f"❌ Test case {i} failed: {e}")
            continue
    
    # Step 4: Market Analysis & Comparison
    logger.info("\n📈 Market Analysis & Insights")
    logger.info("=" * 50)
    
    if all_analyses:
        # Extract analyses for comparison
        analyses_for_comparison = [item['ai_analysis'] for item in all_analyses]
        
        try:
            market_insights = ai_analyzer.compare_opportunities(analyses_for_comparison)
            
            logger.info("🎯 Market Insights:")
            if isinstance(market_insights, dict):
                for key, value in market_insights.items():
                    if key == "salary_analysis" and isinstance(value, dict):
                        logger.info("  💰 Salary Analysis:")
                        for salary_key, salary_value in value.items():
                            logger.info(f"    {salary_key}: {salary_value}")
                    elif key == "skills_analysis" and isinstance(value, dict):
                        logger.info("  🛠️  Skills Analysis:")
                        for skill_key, skill_value in value.items():
                            logger.info(f"    {skill_key}: {skill_value}")
                    elif key == "market_insights" and isinstance(value, list):
                        logger.info("  📊 Market Trends:")
                        for insight in value:
                            logger.info(f"    • {insight}")
                    elif key == "recommendations" and isinstance(value, list):
                        logger.info("  🎯 Recommendations:")
                        for rec in value:
                            logger.info(f"    • {rec}")
            
        except Exception as e:
            logger.error(f"❌ Market analysis failed: {e}")
    
    # Step 5: Export Results
    logger.info("\n💾 Exporting Results")
    logger.info("-" * 30)
    
    try:
        # Ensure data directory exists
        data_dir = Path("data/results")
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Export comprehensive results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Export full analysis
        full_export = {
            "analysis_metadata": {
                "timestamp": datetime.now().isoformat(),
                "total_jobs_analyzed": len(all_analyses),
                "test_cases_completed": len([tc for tc in test_cases if any(a['test_case'] == tc['name'] for a in all_analyses)]),
                "ai_services_used": ["OpenAI GPT-4", "Claude-3.5"]
            },
            "analyses": all_analyses,
            "market_insights": market_insights if 'market_insights' in locals() else {}
        }
        
        full_results_file = data_dir / f"ai_enhanced_analysis_{timestamp}.json"
        with open(full_results_file, 'w', encoding='utf-8') as f:
            json.dump(full_export, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"✅ Full analysis exported to: {full_results_file}")
        
        # Export summary report
        summary_report = {
            "summary": {
                "total_jobs": len(all_analyses),
                "avg_confidence_score": sum(a['ai_analysis'].confidence_score for a in all_analyses) / len(all_analyses) if all_analyses else 0,
                "quality_distribution": {},
                "top_skills": [],
                "salary_ranges": []
            },
            "job_summaries": []
        }
        
        # Calculate quality distribution
        quality_counts = {}
        for analysis in all_analyses:
            quality = analysis['ai_analysis'].analysis_quality
            quality_counts[quality] = quality_counts.get(quality, 0) + 1
        
        summary_report["summary"]["quality_distribution"] = quality_counts
        
        # Add job summaries
        for analysis in all_analyses:
            summary_report["job_summaries"].append({
                "title": analysis['scraped_data']['title'],
                "company": analysis['scraped_data']['company'],
                "confidence_score": analysis['ai_analysis'].confidence_score,
                "quality": analysis['ai_analysis'].analysis_quality,
                "key_highlights": analysis['ai_analysis'].combined_insights.get('key_highlights', [])
            })
        
        summary_file = data_dir / f"analysis_summary_{timestamp}.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Summary report exported to: {summary_file}")
        
    except Exception as e:
        logger.error(f"❌ Export failed: {e}")
    
    # Step 6: Final Summary
    logger.info(f"\n🎉 Analysis Complete!")
    logger.info("=" * 40)
    logger.info(f"📊 Jobs Analyzed: {len(all_analyses)}")
    
    if all_analyses:
        avg_confidence = sum(a['ai_analysis'].confidence_score for a in all_analyses) / len(all_analyses)
        logger.info(f"🎲 Average Confidence: {avg_confidence:.2%}")
        
        # Quality breakdown
        quality_counts = {}
        for analysis in all_analyses:
            quality = analysis['ai_analysis'].analysis_quality
            quality_counts[quality] = quality_counts.get(quality, 0) + 1
        
        logger.info("⭐ Quality Breakdown:")
        for quality, count in quality_counts.items():
            logger.info(f"  {quality.title()}: {count}")
    
    logger.info("\n🚀 Ready for Phase 3: Data Visualization & Analytics!")
    logger.info("Next steps: Build dashboards and statistical analysis")

if __name__ == "__main__":
    test_multi_scraper_with_ai()
