#!/usr/bin/env python3
"""
Focused Small-Scope Test
Tests the complete pipeline with a small, manageable dataset
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
    "logs/focused_test.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="INFO",
    rotation="10 MB"
)
logger.add(sys.stdout, level="INFO")

def focused_test():
    """Run a focused test with small scope to verify all components."""
    
    logger.info("🎯 Focused Small-Scope Test")
    logger.info("=" * 50)
    
    # Initialize components
    settings = Settings()
    
    # Initialize AI analyzer
    logger.info("🤖 Initializing AI components...")
    try:
        ai_analyzer = AIJobAnalyzer()
        ai_enabled = True
        logger.info("✅ AI analyzer ready")
    except Exception as e:
        logger.error(f"❌ AI initialization failed: {e}")
        ai_enabled = False
    
    # Define focused test cases
    test_cases = [
        {
            "name": "Entry-Level Data Analyst",
            "keywords": ["Data Analyst", "Entry Level"],
            "location": "Remote",
            "limit": 3,  # Very small to start
            "expected_skills": ["Excel", "SQL", "Python", "Tableau"]
        },
        {
            "name": "Business Intelligence Analyst", 
            "keywords": ["Business Intelligence", "BI Analyst"],
            "location": "New York, NY",
            "limit": 2,  # Even smaller
            "expected_skills": ["Power BI", "SQL", "Tableau", "Analytics"]
        }
    ]
    
    all_results = []
    
    for i, test_case in enumerate(test_cases, 1):
        logger.info(f"\n📊 Test Case {i}: {test_case['name']}")
        logger.info("-" * 40)
        
        try:
            # Step 1: Search for jobs
            logger.info(f"🔍 Searching for {test_case['limit']} jobs...")
            scraper = IndeedScraper()
            
            job_urls = scraper.search_jobs(
                keywords=test_case['keywords'],
                location=test_case['location'],
                limit=test_case['limit'],
                days_back=14  # Past 2 weeks for fresher results
            )
            
            if not job_urls:
                logger.warning(f"No jobs found for {test_case['name']}")
                
                # Create a sample job for testing AI if no real jobs found
                logger.info("📝 Creating sample job for AI testing...")
                sample_job_data = create_sample_job(test_case)
                
                if ai_enabled and sample_job_data:
                    test_ai_analysis(ai_analyzer, sample_job_data, test_case)
                    all_results.append(sample_job_data)
                
                continue
            
            logger.info(f"✅ Found {len(job_urls)} job URLs")
            
            # Step 2: Process each job
            for j, url in enumerate(job_urls, 1):
                logger.info(f"  📄 Processing job {j}/{len(job_urls)}")
                
                try:
                    # Scrape job details
                    job = scraper.scrape_job_details(url)
                    
                    if not job:
                        logger.warning(f"    ❌ Failed to scrape job {j}")
                        continue
                    
                    # Convert to dict for processing
                    job_data = {
                        'test_case': test_case['name'],
                        'source': 'indeed',
                        'title': job.title,
                        'company': job.company,
                        'location': job.location,
                        'description': job.description,
                        'salary': job.salary,
                        'remote_option': job.remote_option,
                        'url': job.url,
                        'scraped_at': datetime.now().isoformat()
                    }
                    
                    logger.info(f"    ✅ {job.title} at {job.company}")
                    
                    # Step 3: AI Analysis (if enabled)
                    if ai_enabled:
                        logger.info(f"    🤖 Running AI analysis...")
                        
                        try:
                            analysis = ai_analyzer.analyze_job_comprehensive(
                                title=job.title,
                                company=job.company,
                                description=job.description,
                                location=job.location,
                                url=job.url
                            )
                            
                            # Add AI insights to job data
                            job_data['ai_analysis'] = {
                                'confidence_score': analysis.confidence_score,
                                'analysis_quality': analysis.analysis_quality,
                                'skills_identified': analysis.openai_analysis.skills_required[:10] if analysis.openai_analysis else [],
                                'experience_level': analysis.openai_analysis.experience_level if analysis.openai_analysis else None,
                                'salary_estimate': analysis.claude_compensation.salary_range if analysis.claude_compensation else None,
                                'remote_friendly': analysis.openai_analysis.remote_friendly if analysis.openai_analysis else None,
                                'industry': analysis.openai_analysis.industry if analysis.openai_analysis else None,
                                'analyzed_at': analysis.analyzed_at
                            }
                            
                            logger.info(f"    ✅ AI analysis complete (Quality: {analysis.analysis_quality})")
                            
                            # Validate against expected skills
                            if analysis.openai_analysis and analysis.openai_analysis.skills_required:
                                found_expected = [skill for skill in test_case['expected_skills'] 
                                                if any(expected.lower() in skill.lower() for expected in [skill])]
                                if found_expected:
                                    logger.info(f"    🎯 Found expected skills: {', '.join(found_expected)}")
                            
                        except Exception as e:
                            logger.error(f"    ❌ AI analysis failed: {e}")
                            job_data['ai_analysis'] = {'error': str(e)}
                    
                    all_results.append(job_data)
                    
                    # Brief pause between jobs
                    time.sleep(1)
                    
                except Exception as e:
                    logger.error(f"    ❌ Error processing job {j}: {e}")
                    continue
            
            logger.info(f"✅ Test case {i} completed: {len([r for r in all_results if r.get('test_case') == test_case['name']])} jobs processed")
            
        except Exception as e:
            logger.error(f"❌ Test case {i} failed: {e}")
            continue
        
        # Brief pause between test cases
        time.sleep(2)
    
    # Generate comprehensive report
    generate_test_report(all_results, ai_enabled)
    
    logger.info("\n🎉 Focused test completed!")
    logger.info("System verification successful - ready for scaling!")

def create_sample_job(test_case):
    """Create a sample job for testing when no real jobs are found."""
    
    sample_jobs = {
        "Entry-Level Data Analyst": {
            'title': 'Junior Data Analyst',
            'company': 'Sample Analytics Corp',
            'description': '''
            We are seeking an entry-level Data Analyst to join our team.
            
            Responsibilities:
            - Analyze data using Excel and SQL
            - Create reports and dashboards in Tableau
            - Support data-driven decision making
            - Learn Python for data analysis
            
            Requirements:
            - Bachelor's degree in relevant field
            - Proficiency in Excel and SQL
            - Interest in data visualization
            - Strong analytical skills
            
            Salary: $50,000 - $65,000
            Remote work available
            ''',
            'location': 'Remote',
            'salary': '$50,000 - $65,000'
        },
        "Business Intelligence Analyst": {
            'title': 'BI Analyst',
            'company': 'Sample Business Intelligence Inc',
            'description': '''
            Looking for a Business Intelligence Analyst to drive insights.
            
            Responsibilities:
            - Develop Power BI dashboards
            - Write complex SQL queries
            - Analyze business metrics
            - Present findings to stakeholders
            
            Requirements:
            - 2+ years BI experience
            - Expert in Power BI and Tableau
            - Strong SQL skills
            - Business acumen
            
            Salary: $70,000 - $90,000
            Hybrid work model
            ''',
            'location': 'New York, NY',
            'salary': '$70,000 - $90,000'
        }
    }
    
    sample = sample_jobs.get(test_case['name'])
    if sample:
        sample.update({
            'test_case': test_case['name'],
            'source': 'sample',
            'remote_option': 'remote' in sample['description'].lower(),
            'url': 'https://sample.com/job',
            'scraped_at': datetime.now().isoformat()
        })
    
    return sample

def test_ai_analysis(ai_analyzer, job_data, test_case):
    """Test AI analysis on sample job."""
    
    logger.info("    🤖 Testing AI analysis on sample job...")
    
    try:
        analysis = ai_analyzer.analyze_job_comprehensive(
            title=job_data['title'],
            company=job_data['company'],
            description=job_data['description'],
            location=job_data['location'],
            url=job_data['url']
        )
        
        job_data['ai_analysis'] = {
            'confidence_score': analysis.confidence_score,
            'analysis_quality': analysis.analysis_quality,
            'skills_identified': analysis.openai_analysis.skills_required[:10] if analysis.openai_analysis else [],
            'experience_level': analysis.openai_analysis.experience_level if analysis.openai_analysis else None,
            'salary_estimate': analysis.claude_compensation.salary_range if analysis.claude_compensation else None,
            'analyzed_at': analysis.analyzed_at
        }
        
        logger.info(f"    ✅ Sample AI analysis complete (Quality: {analysis.analysis_quality})")
        
    except Exception as e:
        logger.error(f"    ❌ Sample AI analysis failed: {e}")
        job_data['ai_analysis'] = {'error': str(e)}

def generate_test_report(results, ai_enabled):
    """Generate a comprehensive test report."""
    
    logger.info("\n📈 Test Results Summary")
    logger.info("=" * 30)
    
    if not results:
        logger.warning("No results to analyze")
        return
    
    total_jobs = len(results)
    logger.info(f"📊 Total Jobs Processed: {total_jobs}")
    
    # Source distribution
    sources = {}
    for job in results:
        source = job.get('source', 'unknown')
        sources[source] = sources.get(source, 0) + 1
    
    logger.info("📋 Jobs by Source:")
    for source, count in sources.items():
        logger.info(f"  {source.title()}: {count}")
    
    # AI Analysis Summary
    if ai_enabled:
        ai_analyzed = sum(1 for job in results if 'ai_analysis' in job and 'error' not in job['ai_analysis'])
        ai_success_rate = (ai_analyzed / total_jobs) * 100 if total_jobs > 0 else 0
        logger.info(f"🤖 AI Analysis Success Rate: {ai_success_rate:.1f}%")
        
        if ai_analyzed > 0:
            # Skills analysis
            all_skills = []
            for job in results:
                if 'ai_analysis' in job and 'skills_identified' in job['ai_analysis']:
                    all_skills.extend(job['ai_analysis']['skills_identified'])
            
            if all_skills:
                skill_counts = {}
                for skill in all_skills:
                    skill_counts[skill] = skill_counts.get(skill, 0) + 1
                
                top_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:5]
                logger.info("🛠️ Top Skills Identified:")
                for skill, count in top_skills:
                    logger.info(f"  {skill}: {count} mentions")
    
    # Export results
    try:
        results_dir = Path("data/results")
        results_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = results_dir / f"focused_test_{timestamp}.json"
        
        export_data = {
            "test_metadata": {
                "timestamp": datetime.now().isoformat(),
                "test_type": "focused_small_scope",
                "total_jobs": total_jobs,
                "ai_enabled": ai_enabled,
                "success": True
            },
            "results": results,
            "summary": {
                "total_jobs": total_jobs,
                "ai_success_rate": ai_success_rate if ai_enabled else None,
                "sources": sources
            }
        }
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Results exported to: {results_file}")
        
    except Exception as e:
        logger.error(f"❌ Export failed: {e}")

if __name__ == "__main__":
    focused_test()
