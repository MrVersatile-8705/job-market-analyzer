import json
import re
from typing import Dict, List, Optional, Any
from anthropic import Anthropic
from loguru import logger
from dataclasses import dataclass

@dataclass
class CompensationAnalysis:
    """Compensation analysis from Claude."""
    salary_mentioned: bool
    salary_range: Optional[str]
    benefits_mentioned: List[str]
    total_comp_estimate: Optional[str]
    equity_mentioned: bool
    bonus_mentioned: bool
    compensation_competitiveness: str  # low/average/competitive/excellent

@dataclass
class RequirementAnalysis:
    """Detailed requirement analysis."""
    must_have_skills: List[str]
    nice_to_have_skills: List[str]
    education_required: str
    experience_required: str
    certifications_required: List[str]
    industry_experience: List[str]
    domain_knowledge: List[str]

class ClaudeClient:
    """Enhanced Claude client for job market analysis."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-20241022"
    
    def analyze_compensation(self, title: str, company: str, description: str, location: str = "") -> CompensationAnalysis:
        """Analyze compensation and benefits from job posting."""
        
        prompt = f"""
        Analyze the compensation information from this job posting. Focus on extracting and evaluating all compensation-related details.

        Job Title: {title}
        Company: {company}
        Location: {location}
        Description: {description}

        Analyze:
        1. Is salary/compensation explicitly mentioned?
        2. What's the salary range if mentioned?
        3. What benefits are mentioned?
        4. Estimate total compensation value
        5. Is equity/stock options mentioned?
        6. Are bonuses mentioned?
        7. How competitive is this compensation package?

        Return only JSON:
        {{
            "salary_mentioned": true,
            "salary_range": "$90,000 - $130,000",
            "benefits_mentioned": ["health insurance", "401k", "vacation"],
            "total_comp_estimate": "$95,000 - $140,000",
            "equity_mentioned": false,
            "bonus_mentioned": true,
            "compensation_competitiveness": "competitive"
        }}
        """
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=800,
                temperature=0.3,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            result_text = response.content[0].text.strip()
            
            # Clean up JSON
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                result_text = result_text.split("```")[1]
            
            result_data = json.loads(result_text)
            return CompensationAnalysis(**result_data)
            
        except Exception as e:
            logger.error(f"Error analyzing compensation with Claude: {e}")
            return CompensationAnalysis(
                salary_mentioned=False,
                salary_range=None,
                benefits_mentioned=[],
                total_comp_estimate=None,
                equity_mentioned=False,
                bonus_mentioned=False,
                compensation_competitiveness="unknown"
            )
    
    def analyze_requirements_detailed(self, description: str) -> RequirementAnalysis:
        """Detailed analysis of job requirements and qualifications."""
        
        prompt = f"""
        Analyze this job description and extract detailed requirement information. Categorize requirements by importance and type.

        Description: {description}

        Extract and categorize:
        1. Must-have skills (absolutely required)
        2. Nice-to-have skills (preferred but not required)
        3. Education requirements
        4. Experience requirements (years and type)
        5. Required certifications
        6. Industry experience needed
        7. Domain knowledge requirements

        Return only JSON:
        {{
            "must_have_skills": ["Python", "SQL", "Statistics"],
            "nice_to_have_skills": ["R", "Tableau", "AWS"],
            "education_required": "Bachelor's degree in related field",
            "experience_required": "3-5 years data analysis experience",
            "certifications_required": ["None specified"],
            "industry_experience": ["Technology", "Financial Services"],
            "domain_knowledge": ["Data visualization", "Statistical analysis"]
        }}
        """
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.2,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            result_text = response.content[0].text.strip()
            
            # Clean up JSON
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                result_text = result_text.split("```")[1]
            
            result_data = json.loads(result_text)
            return RequirementAnalysis(**result_data)
            
        except Exception as e:
            logger.error(f"Error analyzing requirements with Claude: {e}")
            return RequirementAnalysis(
                must_have_skills=[],
                nice_to_have_skills=[],
                education_required="Not specified",
                experience_required="Not specified",
                certifications_required=[],
                industry_experience=[],
                domain_knowledge=[]
            )
    
    def analyze_company_culture(self, company: str, description: str) -> Dict[str, Any]:
        """Analyze company culture and work environment from job posting."""
        
        prompt = f"""
        Analyze the company culture and work environment from this job posting.

        Company: {company}
        Job Description: {description}

        Analyze:
        1. Work environment (remote/hybrid/office)
        2. Company culture indicators
        3. Team dynamics mentioned
        4. Growth opportunities
        5. Work-life balance indicators
        6. Company values mentioned
        7. Diversity and inclusion mentions

        Return JSON:
        {{
            "work_environment": "hybrid",
            "culture_keywords": ["collaborative", "innovative", "fast-paced"],
            "team_dynamics": "cross-functional teams",
            "growth_opportunities": ["mentorship", "training", "promotion paths"],
            "work_life_balance": "flexible hours mentioned",
            "company_values": ["innovation", "customer focus"],
            "diversity_inclusion": true,
            "remote_flexibility": "hybrid work available"
        }}
        """
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=800,
                temperature=0.3,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            result_text = response.content[0].text.strip()
            
            # Clean up JSON
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                result_text = result_text.split("```")[1]
            
            return json.loads(result_text)
            
        except Exception as e:
            logger.error(f"Error analyzing company culture: {e}")
            return {
                "work_environment": "unknown",
                "culture_keywords": [],
                "team_dynamics": "unknown",
                "growth_opportunities": [],
                "work_life_balance": "unknown",
                "company_values": [],
                "diversity_inclusion": False,
                "remote_flexibility": "unknown"
            }
    
    def compare_job_postings(self, jobs: List[Dict]) -> Dict[str, Any]:
        """Compare multiple job postings and provide insights."""
        
        jobs_text = ""
        for i, job in enumerate(jobs, 1):
            jobs_text += f"""
            Job {i}:
            Title: {job.get('title', '')}
            Company: {job.get('company', '')}
            Location: {job.get('location', '')}
            Salary: {job.get('salary', 'Not specified')}
            Description: {job.get('description', '')[:500]}...
            
            """
        
        prompt = f"""
        Compare these job postings and provide insights about market trends, compensation differences, and requirements variations.

        {jobs_text}

        Analyze:
        1. Salary ranges comparison
        2. Common skills across postings
        3. Unique requirements per job
        4. Company size/type patterns
        5. Location impact on compensation
        6. Industry trends observed
        7. Best opportunities identified

        Return detailed JSON analysis:
        {{
            "salary_analysis": {{
                "min_salary": "$70,000",
                "max_salary": "$150,000",
                "average_estimate": "$110,000",
                "location_premium": "NYC jobs 20% higher"
            }},
            "skills_analysis": {{
                "most_common": ["Python", "SQL", "Excel"],
                "emerging_trends": ["MLOps", "Cloud platforms"],
                "rare_valuable": ["Specialized domain knowledge"]
            }},
            "market_insights": ["Remote work widely available", "Strong demand for ML skills"],
            "best_opportunities": [1, 3],
            "recommendations": ["Focus on cloud skills", "Consider remote positions"]
        }}
        """
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.3,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            result_text = response.content[0].text.strip()
            
            # Clean up JSON
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                result_text = result_text.split("```")[1]
            
            return json.loads(result_text)
            
        except Exception as e:
            logger.error(f"Error comparing job postings: {e}")
            return {
                "salary_analysis": {},
                "skills_analysis": {},
                "market_insights": [],
                "best_opportunities": [],
                "recommendations": []
            }