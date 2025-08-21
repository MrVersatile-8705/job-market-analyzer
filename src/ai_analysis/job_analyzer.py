"""
AI Job Analysis Orchestrator

This module combines OpenAI and Claude AI services to provide comprehensive
job market analysis with multiple AI perspectives.
"""

import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from loguru import logger

try:
    from .openai_client import OpenAIClient, JobAnalysis
    from .claude_client import ClaudeClient, CompensationAnalysis, RequirementAnalysis
    from ..config.settings import Settings
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from ai_analysis.openai_client import OpenAIClient, JobAnalysis
    from ai_analysis.claude_client import ClaudeClient, CompensationAnalysis, RequirementAnalysis
    from config.settings import Settings

@dataclass
class ComprehensiveJobAnalysis:
    """Complete analysis combining multiple AI perspectives."""
    # Basic job info
    title: str
    company: str
    location: str
    url: str
    analyzed_at: str
    
    # OpenAI Analysis
    openai_analysis: JobAnalysis
    
    # Claude Analysis
    claude_compensation: CompensationAnalysis
    claude_requirements: RequirementAnalysis
    claude_culture: Dict[str, Any]
    
    # Combined insights
    combined_insights: Dict[str, Any]
    confidence_score: float
    analysis_quality: str

class AIJobAnalyzer:
    """Orchestrates multiple AI services for comprehensive job analysis."""
    
    def __init__(self):
        self.settings = Settings()
        self.openai_client = None
        self.claude_client = None
        
        # Initialize AI clients if API keys are available
        try:
            if self.settings.OPENAI_API_KEY:
                self.openai_client = OpenAIClient(self.settings.OPENAI_API_KEY)
                logger.info("OpenAI client initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize OpenAI client: {e}")
        
        try:
            if self.settings.CLAUDE_API_KEY:
                self.claude_client = ClaudeClient(self.settings.CLAUDE_API_KEY)
                logger.info("Claude client initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize Claude client: {e}")
    
    def analyze_job_comprehensive(self, 
                                title: str, 
                                company: str, 
                                description: str, 
                                location: str = "",
                                url: str = "") -> ComprehensiveJobAnalysis:
        """
        Perform comprehensive analysis using all available AI services.
        
        Args:
            title: Job title
            company: Company name
            description: Job description text
            location: Job location
            url: Job posting URL
            
        Returns:
            ComprehensiveJobAnalysis with results from multiple AI services
        """
        logger.info(f"Starting comprehensive analysis for: {title} at {company}")
        
        # OpenAI Analysis
        openai_analysis = None
        if self.openai_client:
            try:
                openai_analysis = self.openai_client.analyze_job_posting(
                    title, company, description, location
                )
                logger.info("OpenAI analysis completed")
            except Exception as e:
                logger.error(f"OpenAI analysis failed: {e}")
        
        # Claude Analysis
        claude_compensation = None
        claude_requirements = None
        claude_culture = None
        
        if self.claude_client:
            try:
                claude_compensation = self.claude_client.analyze_compensation(
                    title, company, description, location
                )
                logger.info("Claude compensation analysis completed")
                
                claude_requirements = self.claude_client.analyze_requirements_detailed(description)
                logger.info("Claude requirements analysis completed")
                
                claude_culture = self.claude_client.analyze_company_culture(company, description)
                logger.info("Claude culture analysis completed")
                
            except Exception as e:
                logger.error(f"Claude analysis failed: {e}")
        
        # Generate combined insights
        combined_insights = self._generate_combined_insights(
            openai_analysis, claude_compensation, claude_requirements, claude_culture
        )
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(
            openai_analysis, claude_compensation, claude_requirements
        )
        
        # Determine analysis quality
        analysis_quality = self._determine_analysis_quality(confidence_score, 
                                                          openai_analysis, 
                                                          claude_compensation)
        
        return ComprehensiveJobAnalysis(
            title=title,
            company=company,
            location=location,
            url=url,
            analyzed_at=datetime.now().isoformat(),
            openai_analysis=openai_analysis,
            claude_compensation=claude_compensation,
            claude_requirements=claude_requirements,
            claude_culture=claude_culture,
            combined_insights=combined_insights,
            confidence_score=confidence_score,
            analysis_quality=analysis_quality
        )
    
    def batch_analyze_jobs(self, jobs: List[Dict]) -> List[ComprehensiveJobAnalysis]:
        """Analyze multiple jobs in batch."""
        results = []
        
        for i, job in enumerate(jobs, 1):
            logger.info(f"Analyzing job {i}/{len(jobs)}: {job.get('title', 'Unknown')}")
            
            try:
                analysis = self.analyze_job_comprehensive(
                    title=job.get('title', ''),
                    company=job.get('company', ''),
                    description=job.get('description', ''),
                    location=job.get('location', ''),
                    url=job.get('url', '')
                )
                results.append(analysis)
                
            except Exception as e:
                logger.error(f"Failed to analyze job {i}: {e}")
                continue
        
        return results
    
    def compare_opportunities(self, analyses: List[ComprehensiveJobAnalysis]) -> Dict[str, Any]:
        """Compare multiple job analyses and provide market insights."""
        if not analyses:
            return {"error": "No analyses provided"}
        
        if self.claude_client:
            try:
                # Prepare job data for Claude comparison
                jobs_for_comparison = []
                for analysis in analyses:
                    jobs_for_comparison.append({
                        'title': analysis.title,
                        'company': analysis.company,
                        'location': analysis.location,
                        'salary': getattr(analysis.claude_compensation, 'salary_range', None) if analysis.claude_compensation else None,
                        'description': f"Skills: {', '.join(analysis.openai_analysis.skills_required[:5]) if analysis.openai_analysis else 'Unknown'}"
                    })
                
                comparison = self.claude_client.compare_job_postings(jobs_for_comparison)
                return comparison
                
            except Exception as e:
                logger.error(f"Job comparison failed: {e}")
        
        # Fallback comparison logic
        return self._basic_comparison(analyses)
    
    def _generate_combined_insights(self, 
                                  openai_analysis: Optional[JobAnalysis],
                                  claude_compensation: Optional[CompensationAnalysis],
                                  claude_requirements: Optional[RequirementAnalysis],
                                  claude_culture: Optional[Dict]) -> Dict[str, Any]:
        """Generate insights by combining analyses from different AI services."""
        
        insights = {
            "skill_consensus": [],
            "salary_insights": {},
            "requirement_difficulty": "unknown",
            "opportunity_rating": "unknown",
            "key_highlights": [],
            "potential_concerns": []
        }
        
        try:
            # Skill consensus between OpenAI and Claude
            if openai_analysis and claude_requirements:
                openai_skills = set(openai_analysis.skills_required + openai_analysis.skills_preferred)
                claude_skills = set(claude_requirements.must_have_skills + claude_requirements.nice_to_have_skills)
                
                insights["skill_consensus"] = list(openai_skills.intersection(claude_skills))
            
            # Salary insights
            if claude_compensation:
                insights["salary_insights"] = {
                    "explicitly_mentioned": claude_compensation.salary_mentioned,
                    "estimated_range": claude_compensation.salary_range,
                    "total_comp_competitive": claude_compensation.compensation_competitiveness,
                    "benefits_count": len(claude_compensation.benefits_mentioned)
                }
            
            # Requirement difficulty assessment
            if claude_requirements:
                must_have_count = len(claude_requirements.must_have_skills)
                nice_to_have_count = len(claude_requirements.nice_to_have_skills)
                
                if must_have_count <= 3:
                    insights["requirement_difficulty"] = "entry_friendly"
                elif must_have_count <= 6:
                    insights["requirement_difficulty"] = "moderate"
                else:
                    insights["requirement_difficulty"] = "experienced_required"
            
            # Opportunity rating
            if openai_analysis:
                growth_potential = openai_analysis.growth_potential.lower()
                remote_friendly = openai_analysis.remote_friendly
                
                if growth_potential == "high" and remote_friendly:
                    insights["opportunity_rating"] = "excellent"
                elif growth_potential in ["high", "medium"] or remote_friendly:
                    insights["opportunity_rating"] = "good"
                else:
                    insights["opportunity_rating"] = "average"
            
            # Key highlights
            highlights = []
            if openai_analysis and openai_analysis.remote_friendly:
                highlights.append("Remote work available")
            if claude_compensation and claude_compensation.equity_mentioned:
                highlights.append("Equity compensation offered")
            if openai_analysis and openai_analysis.growth_potential == "high":
                highlights.append("High growth potential")
            
            insights["key_highlights"] = highlights
            
            # Potential concerns
            concerns = []
            if claude_compensation and not claude_compensation.salary_mentioned:
                concerns.append("Salary not disclosed")
            if claude_requirements and len(claude_requirements.must_have_skills) > 8:
                concerns.append("Extensive skill requirements")
            
            insights["potential_concerns"] = concerns
            
        except Exception as e:
            logger.error(f"Error generating combined insights: {e}")
        
        return insights
    
    def _calculate_confidence_score(self, 
                                  openai_analysis: Optional[JobAnalysis],
                                  claude_compensation: Optional[CompensationAnalysis],
                                  claude_requirements: Optional[RequirementAnalysis]) -> float:
        """Calculate confidence score based on analysis completeness and consistency."""
        
        score = 0.0
        max_score = 0.0
        
        # OpenAI analysis completeness (40% of total)
        if openai_analysis:
            max_score += 0.4
            if openai_analysis.skills_required:
                score += 0.1
            if openai_analysis.experience_level != "unknown":
                score += 0.1
            if openai_analysis.industry != "unknown":
                score += 0.1
            if openai_analysis.key_responsibilities:
                score += 0.1
        
        # Claude compensation analysis (30% of total)
        if claude_compensation:
            max_score += 0.3
            if claude_compensation.salary_mentioned:
                score += 0.15
            if claude_compensation.benefits_mentioned:
                score += 0.1
            if claude_compensation.compensation_competitiveness != "unknown":
                score += 0.05
        
        # Claude requirements analysis (30% of total)
        if claude_requirements:
            max_score += 0.3
            if claude_requirements.must_have_skills:
                score += 0.15
            if claude_requirements.education_required != "Not specified":
                score += 0.1
            if claude_requirements.experience_required != "Not specified":
                score += 0.05
        
        return score / max_score if max_score > 0 else 0.0
    
    def _determine_analysis_quality(self, 
                                  confidence_score: float,
                                  openai_analysis: Optional[JobAnalysis],
                                  claude_compensation: Optional[CompensationAnalysis]) -> str:
        """Determine overall analysis quality rating."""
        
        if confidence_score >= 0.8:
            return "excellent"
        elif confidence_score >= 0.6:
            return "good"
        elif confidence_score >= 0.4:
            return "fair"
        else:
            return "limited"
    
    def _basic_comparison(self, analyses: List[ComprehensiveJobAnalysis]) -> Dict[str, Any]:
        """Basic fallback comparison when Claude is not available."""
        
        if not analyses:
            return {}
        
        skills_frequency = {}
        companies = set()
        locations = set()
        remote_count = 0
        
        for analysis in analyses:
            companies.add(analysis.company)
            locations.add(analysis.location)
            
            if analysis.openai_analysis:
                if analysis.openai_analysis.remote_friendly:
                    remote_count += 1
                
                for skill in analysis.openai_analysis.skills_required:
                    skills_frequency[skill] = skills_frequency.get(skill, 0) + 1
        
        most_common_skills = sorted(skills_frequency.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_jobs": len(analyses),
            "unique_companies": len(companies),
            "unique_locations": len(locations),
            "remote_percentage": (remote_count / len(analyses)) * 100,
            "most_common_skills": [skill for skill, count in most_common_skills],
            "analysis_method": "basic_comparison"
        }
    
    def export_analysis(self, analysis: ComprehensiveJobAnalysis, filepath: str):
        """Export analysis to JSON file."""
        try:
            # Convert dataclass to dictionary
            analysis_dict = asdict(analysis)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(analysis_dict, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Analysis exported to {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to export analysis: {e}")
    
    def get_analysis_summary(self, analysis: ComprehensiveJobAnalysis) -> str:
        """Generate a human-readable summary of the analysis."""
        
        summary_parts = []
        
        # Basic info
        summary_parts.append(f"🎯 Position: {analysis.title} at {analysis.company}")
        summary_parts.append(f"📍 Location: {analysis.location}")
        summary_parts.append(f"⭐ Analysis Quality: {analysis.analysis_quality.title()}")
        summary_parts.append(f"🎲 Confidence: {analysis.confidence_score:.2%}")
        
        # Key insights
        if analysis.combined_insights.get("key_highlights"):
            summary_parts.append("✨ Highlights:")
            for highlight in analysis.combined_insights["key_highlights"]:
                summary_parts.append(f"  • {highlight}")
        
        # Skills
        if analysis.openai_analysis and analysis.openai_analysis.skills_required:
            top_skills = analysis.openai_analysis.skills_required[:5]
            summary_parts.append(f"🛠️  Key Skills: {', '.join(top_skills)}")
        
        # Compensation
        if analysis.claude_compensation and analysis.claude_compensation.salary_range:
            summary_parts.append(f"💰 Salary: {analysis.claude_compensation.salary_range}")
        
        # Concerns
        if analysis.combined_insights.get("potential_concerns"):
            summary_parts.append("⚠️  Concerns:")
            for concern in analysis.combined_insights["potential_concerns"]:
                summary_parts.append(f"  • {concern}")
        
        return "\n".join(summary_parts)

if __name__ == "__main__":
    # Test the analyzer
    analyzer = AIJobAnalyzer()
    
    # Sample job for testing
    test_job = {
        "title": "Senior Data Analyst",
        "company": "TechCorp Inc.",
        "description": """
        We are seeking a Senior Data Analyst to join our growing analytics team. 
        The ideal candidate will have 5+ years of experience with Python, SQL, and Tableau.
        Responsibilities include building dashboards, analyzing customer data, and 
        presenting insights to stakeholders. Competitive salary and benefits package.
        Remote work options available.
        """,
        "location": "San Francisco, CA"
    }
    
    try:
        analysis = analyzer.analyze_job_comprehensive(
            test_job["title"],
            test_job["company"],
            test_job["description"],
            test_job["location"]
        )
        
        print(analyzer.get_analysis_summary(analysis))
        
    except Exception as e:
        print(f"Test failed: {e}")
