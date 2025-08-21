import json
import re
from typing import Dict, List, Optional, Tuple
from openai import OpenAI
from loguru import logger
from dataclasses import dataclass

@dataclass
class JobAnalysis:
    """Structured analysis result from AI."""
    skills_required: List[str]
    skills_preferred: List[str]
    experience_level: str
    salary_estimate: Optional[str]
    remote_friendly: bool
    industry: str
    role_category: str
    key_responsibilities: List[str]
    requirements_technical: List[str]
    requirements_soft: List[str]
    company_size_estimate: Optional[str]
    growth_potential: str
    
class OpenAIClient:
    """Enhanced OpenAI client for comprehensive job analysis."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o"  # Using latest GPT-4
    
    def analyze_job_posting(self, title: str, company: str, description: str, location: str = "") -> JobAnalysis:
        """Comprehensive analysis of a job posting using GPT-4."""
        
        prompt = f"""
        Analyze this job posting and provide structured information. Respond in JSON format only.

        Job Title: {title}
        Company: {company}
        Location: {location}
        Description: {description}

        Extract and analyze:
        1. Skills (separate required vs preferred)
        2. Experience level (entry/junior/mid/senior/executive)
        3. Salary estimate if mentioned (or "not specified")
        4. Remote work friendliness (true/false)
        5. Industry classification
        6. Role category (analyst/engineer/scientist/manager/etc)
        7. Key responsibilities (top 5)
        8. Technical requirements
        9. Soft skill requirements
        10. Company size estimate (startup/small/medium/large/enterprise)
        11. Growth potential (low/medium/high)

        Return JSON:
        {{
            "skills_required": ["skill1", "skill2"],
            "skills_preferred": ["skill1", "skill2"],
            "experience_level": "mid",
            "salary_estimate": "$80,000 - $120,000",
            "remote_friendly": true,
            "industry": "Technology",
            "role_category": "Data Analyst",
            "key_responsibilities": ["responsibility1", "responsibility2"],
            "requirements_technical": ["requirement1", "requirement2"],
            "requirements_soft": ["requirement1", "requirement2"],
            "company_size_estimate": "medium",
            "growth_potential": "high"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert job market analyst. Provide detailed, accurate analysis in valid JSON format only."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Clean up the response to extract JSON
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                result_text = result_text.split("```")[1]
            
            result_data = json.loads(result_text)
            
            return JobAnalysis(**result_data)
            
        except Exception as e:
            logger.error(f"Error analyzing job posting with OpenAI: {e}")
            # Return default analysis
            return JobAnalysis(
                skills_required=[],
                skills_preferred=[],
                experience_level="unknown",
                salary_estimate=None,
                remote_friendly=False,
                industry="unknown",
                role_category="unknown",
                key_responsibilities=[],
                requirements_technical=[],
                requirements_soft=[],
                company_size_estimate=None,
                growth_potential="unknown"
            )
    
    def extract_skills_detailed(self, description: str) -> Dict[str, List[str]]:
        """Extract and categorize skills from job description."""
        
        prompt = f"""
        Extract all skills from this job description and categorize them. Return JSON only.

        Description: {description}

        Categorize into:
        - programming_languages: Python, R, SQL, etc.
        - tools_software: Tableau, Excel, AWS, etc.
        - methodologies: Agile, Machine Learning, Statistics, etc.
        - soft_skills: Communication, Leadership, etc.
        - certifications: AWS Certified, Google Analytics, etc.

        JSON format:
        {{
            "programming_languages": ["Python", "SQL"],
            "tools_software": ["Tableau", "Excel"],
            "methodologies": ["Machine Learning", "Statistics"],
            "soft_skills": ["Communication", "Problem Solving"],
            "certifications": ["AWS Certified"]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a skill extraction expert. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.2
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Clean up JSON
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                result_text = result_text.split("```")[1]
            
            return json.loads(result_text)
            
        except Exception as e:
            logger.error(f"Error extracting skills: {e}")
            return {
                "programming_languages": [],
                "tools_software": [],
                "methodologies": [],
                "soft_skills": [],
                "certifications": []
            }
    
    def estimate_salary_range(self, title: str, location: str, description: str) -> Dict[str, str]:
        """Estimate salary range based on job details."""
        
        prompt = f"""
        Estimate the salary range for this position. Consider market rates, location, and requirements.

        Job Title: {title}
        Location: {location}
        Description: {description}

        Provide estimate in JSON:
        {{
            "salary_min": "80000",
            "salary_max": "120000",
            "currency": "USD",
            "period": "annual",
            "confidence": "medium",
            "factors": ["location", "experience_required", "skills_premium"]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a compensation analyst. Provide realistic salary estimates based on current market data."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Clean up JSON
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                result_text = result_text.split("```")[1]
            
            return json.loads(result_text)
            
        except Exception as e:
            logger.error(f"Error estimating salary: {e}")
            return {
                "salary_min": "unknown",
                "salary_max": "unknown",
                "currency": "USD",
                "period": "annual",
                "confidence": "low",
                "factors": []
            }
    
    def classify_job_level(self, title: str, description: str) -> Dict[str, str]:
        """Classify job seniority level and career stage."""
        
        prompt = f"""
        Classify the seniority level of this position.

        Title: {title}
        Description: {description}

        Return JSON:
        {{
            "seniority_level": "mid",
            "experience_years_min": "3",
            "experience_years_max": "5",
            "career_stage": "individual_contributor",
            "management_level": "none",
            "reasoning": "Requires 3-5 years experience, IC role"
        }}

        Seniority levels: entry, junior, mid, senior, staff, principal, director, vp, c_level
        Career stages: entry_level, individual_contributor, team_lead, manager, senior_manager, director, executive
        Management levels: none, team_lead, manager, senior_manager, director, vp, c_level
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an HR expert specializing in job level classification."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.2
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Clean up JSON
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                result_text = result_text.split("```")[1]
            
            return json.loads(result_text)
            
        except Exception as e:
            logger.error(f"Error classifying job level: {e}")
            return {
                "seniority_level": "unknown",
                "experience_years_min": "0",
                "experience_years_max": "0",
                "career_stage": "unknown",
                "management_level": "unknown",
                "reasoning": "Analysis failed"
            }