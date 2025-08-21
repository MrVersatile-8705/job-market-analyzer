#!/usr/bin/env python3
"""
Quick AI Test with Credits Added
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from loguru import logger
from src.ai_analysis.job_analyzer import AIJobAnalyzer

# Configure simple logging
logger.remove()
logger.add(sys.stdout, level="INFO")

def test_ai_with_credits():
    """Test AI analysis with credits added."""
    
    logger.info("🚀 Testing AI Analysis with Credits")
    logger.info("=" * 40)
    
    # Sample job posting for testing
    sample_job = {
        'title': 'Senior Data Scientist',
        'company': 'Meta',
        'description': '''
        We are looking for a Senior Data Scientist to join our AI Research team. 
        
        Responsibilities:
        - Develop machine learning models for recommendation systems
        - Analyze large datasets using Python, SQL, and Spark
        - Collaborate with cross-functional teams
        - Build predictive models for user engagement
        
        Requirements:
        - 5+ years experience in data science
        - Master's degree in Computer Science, Statistics, or related field
        - Proficiency in Python, R, SQL
        - Experience with TensorFlow, PyTorch
        - Strong statistical analysis skills
        - Experience with A/B testing
        
        Benefits:
        - Competitive salary: $180,000 - $250,000
        - Stock options
        - Health insurance
        - Remote work flexibility
        ''',
        'location': 'San Francisco, CA',
        'url': 'https://example.com/job/123'
    }
    
    try:
        # Initialize AI analyzer
        logger.info("🤖 Initializing AI analyzer...")
        ai_analyzer = AIJobAnalyzer()
        
        # Test comprehensive analysis
        logger.info("📊 Running comprehensive AI analysis...")
        analysis = ai_analyzer.analyze_job_comprehensive(
            title=sample_job['title'],
            company=sample_job['company'],
            description=sample_job['description'],
            location=sample_job['location'],
            url=sample_job['url']
        )
        
        # Display results
        logger.info("✅ AI Analysis Complete!")
        logger.info(f"📈 Confidence Score: {analysis.confidence_score:.2%}")
        logger.info(f"⭐ Analysis Quality: {analysis.analysis_quality}")
        
        if analysis.openai_analysis:
            logger.info("\n🧠 OpenAI Analysis:")
            logger.info(f"   Industry: {analysis.openai_analysis.industry}")
            logger.info(f"   Experience Level: {analysis.openai_analysis.experience_level}")
            logger.info(f"   Remote Friendly: {analysis.openai_analysis.remote_friendly}")
            logger.info(f"   Top Skills: {', '.join(analysis.openai_analysis.skills_required[:5])}")
        
        if analysis.claude_compensation:
            logger.info("\n💰 Claude Compensation Analysis:")
            logger.info(f"   Salary Range: {analysis.claude_compensation.salary_range}")
            logger.info(f"   Total Comp: {analysis.claude_compensation.total_comp_estimate}")
            logger.info(f"   Benefits: {', '.join(analysis.claude_compensation.benefits_mentioned[:3])}")
            logger.info(f"   Competitiveness: {analysis.claude_compensation.compensation_competitiveness}")
        
        if analysis.claude_requirements:
            logger.info("\n📋 Claude Requirements Analysis:")
            logger.info(f"   Education: {analysis.claude_requirements.education_required}")
            logger.info(f"   Must-Have Skills: {', '.join(analysis.claude_requirements.must_have_skills[:3])}")
            logger.info(f"   Experience: {analysis.claude_requirements.experience_required}")
        
        logger.info("\n🎯 Combined Insights:")
        for key, value in analysis.combined_insights.items():
            if isinstance(value, list):
                logger.info(f"   {key}: {', '.join(map(str, value[:3]))}")
            else:
                logger.info(f"   {key}: {value}")
                
        logger.info("\n🎉 AI testing successful! Both APIs are working.")
        
    except Exception as e:
        logger.error(f"❌ AI test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ai_with_credits()
