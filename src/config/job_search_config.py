#!/usr/bin/env python3
"""
Comprehensive Job Search Configuration
Contains all job titles and search strategies for enhanced job market analysis
Supports multiple scrapers: Indeed, ZipRecruiter, Dice, StackOverflow, Builtin
"""

# Comprehensive list of analytics and data-related job titles
ANALYTICS_JOB_TITLES = [
    "Data Analyst",
    "Data Scientist", 
    "Analytics Engineer",
    "BI Developer",
    "BI Analyst",
    "Reporting & Insights Specialist",
    "Strategy Analyst",
    "Business Strategy Manager",
    "Operations Analyst",
    "Product Analytics Manager",
    # Additional related titles for broader coverage
    "Business Analyst",
    "Business Intelligence Analyst",
    "Data Engineer",
    "Quantitative Analyst",
    "Financial Analyst",
    "Marketing Analyst",
    "Sales Analyst",
    "Research Analyst",
    "Insights Analyst",
    "Performance Analyst"
]

# Available scraper platforms
AVAILABLE_SCRAPERS = {
    "indeed": {
        "name": "Indeed",
        "class": "IndeedScraper",
        "strengths": ["High volume", "All experience levels", "Geographic coverage"],
        "best_for": ["General analytics roles", "Entry to mid-level positions"]
    },
    "ziprecruiter": {
        "name": "ZipRecruiter", 
        "class": "ZipRecruiterScraper",
        "strengths": ["Large volume", "Quick application process", "Mobile-first"],
        "best_for": ["Quick-fill positions", "SMB companies", "Contract work"]
    },
    "dice": {
        "name": "Dice",
        "class": "DiceScraper", 
        "strengths": ["Tech-focused", "High salaries", "Contract opportunities"],
        "best_for": ["Data engineering", "Technical analytics", "Contract positions"]
    },
    "stackoverflow": {
        "name": "StackOverflow",
        "class": "StackOverflowScraper",
        "strengths": ["Developer-focused", "High-quality roles", "Startup to enterprise"],
        "best_for": ["Technical data roles", "Engineering-adjacent positions"]
    },
    "builtin": {
        "name": "Builtin",
        "class": "BuiltinScraper",
        "strengths": ["Startup ecosystem", "Equity compensation", "Growth companies"],
        "best_for": ["Startup analytics", "Product analytics", "Growth-stage companies"]
    }
}

# Grouped search strategies for different scenarios
SEARCH_SCENARIOS = {
    "core_analytics": {
        "titles": ["Data Analyst", "Business Analyst", "Analytics Engineer"],
        "description": "Core analytics positions across industries"
    },
    "business_intelligence": {
        "titles": ["BI Developer", "BI Analyst", "Business Intelligence Analyst"],
        "description": "Business Intelligence and reporting focused roles"
    },
    "data_science": {
        "titles": ["Data Scientist", "Data Engineer", "Quantitative Analyst"],
        "description": "Advanced data science and engineering positions"
    },
    "strategy_operations": {
        "titles": ["Strategy Analyst", "Business Strategy Manager", "Operations Analyst"],
        "description": "Strategic and operational analytics roles"
    },
    "specialized_analytics": {
        "titles": ["Product Analytics Manager", "Reporting & Insights Specialist", "Performance Analyst"],
        "description": "Specialized analytics and insights positions"
    },
    "domain_specific": {
        "titles": ["Financial Analyst", "Marketing Analyst", "Sales Analyst"],
        "description": "Domain-specific analyst roles"
    }
}

# Enhanced search configurations for different analysis types
ENHANCED_SEARCH_CONFIGS = [
    {
        "name": "Comprehensive Data Analytics - Remote Focus",
        "keywords": ["Data Analyst", "Business Analyst", "Analytics Engineer"],
        "location": "",  # No location for remote focus
        "limit": 30,
        "days_back": 90,
        "priority": "high"
    },
    {
        "name": "Business Intelligence Specialists - Major Markets",
        "keywords": ["BI Developer", "BI Analyst", "Business Intelligence"],
        "location": "",# No location for remote focus
        "limit": 25,
        "days_back": 90,
        "priority": "high"
    },
    {
        "name": "Data Science & Advanced Analytics - Tech Hubs",
        "keywords": ["Data Scientist", "Quantitative Analyst", "Data Engineer"],
        "location": "",  # No location for remote focus
        "limit": 25,
        "days_back": 90,
        "priority": "high"
    },
    {
        "name": "Strategy & Operations Analytics - Healthcare Industry",
        "keywords": ["Strategy Analyst", "Business Analytics Manager", "Operations Analyst"],
        "location": "",  # No location for remote focus
        "limit": 20,
        "days_back": 90,
        "priority": "medium"
    },
    {
        "name": "Product & Performance Analytics - Nationwide",
        "keywords": ["Product Analytics Manager", "Performance Analyst", "Insights Analyst"],
        "location": "",
        "limit": 20,
        "days_back": 90,
        "priority": "medium"
    },
    {
        "name": "Reporting & Insights Specialists - Nationwide",
        "keywords": ["Reporting & Insights Specialist", "Research Analyst", "Marketing Analyst"],
        "location": "",  # No location for remote focus
        "limit": 15,
        "days_back": 90,
        "priority": "medium"
    }
]

# Working search configurations (proven to find jobs)
WORKING_SEARCH_CONFIGS = [
    {
        "name": "Data Analyst Positions - Cleveland Market",
        "keywords": ["Data Analyst"],
        "location": "Cleveland, OH",
        "limit": 25,
        "days_back": 90,
    },
    {
        "name": "Business Intelligence - Nationwide",
        "keywords": ["Business Intelligence", "BI Analyst"],
        "location": "",  # No location for remote focus
        "limit": 25,
        "days_back": 90,
    },
    {
        "name": "Analytics Engineers - Remote Positions",
        "keywords": ["Analytics Engineer", "Data Engineer"],
        "location": "Remote",
        "limit": 25,
        "days_back": 90,
    },
    {
        "name": "Strategy Analysts - National Search",
        "keywords": ["Strategy Analyst", "Business Strategy Manager"],
        "location": "",
        "limit": 25,
        "days_back": 90,
    }
]

# Focused test configurations for validation
FOCUSED_TEST_CONFIGS = [
    {
        "name": "Mid-Level Data Analyst",
        "keywords": ["Data Analyst", "Mid Level"],
        "location": "Remote",
        "limit": 3,
        "expected_skills": ["Excel", "SQL", "Python", "Tableau"]
    },
    {
        "name": "Business Intelligence Analyst",
        "keywords": ["Business Intelligence", "BI Analyst"],
        "location": "", 
        "limit": 2,
        "expected_skills": ["Power BI", "SQL", "Tableau", "Analytics"]
    },
    {
        "name": "Analytics Engineer",
        "keywords": ["Analytics Engineer", "Data Engineer"],
        "location": "",
        "limit": 2,
        "expected_skills": ["SQL", "Python", "dbt", "Cloud Platforms"]
    },
    {
        "name": "Strategy Analyst",
        "keywords": ["Strategy Analyst", "Business Strategy"],
        "location": "",
        "limit": 2,
        "expected_skills": ["Excel", "PowerPoint", "Strategic Planning", "Analytics"]
    },
    {
        "name": "Product Analytics Manager",
        "keywords": ["Product Analytics Manager", "Product Analyst"],
        "location": "",
        "limit": 1,
        "expected_skills": ["Analytics", "Product Management", "SQL", "A/B Testing"]
    }
]

def get_all_job_titles():
    """Get the complete list of analytics job titles."""
    return ANALYTICS_JOB_TITLES

def get_available_scrapers():
    """Get information about all available scrapers."""
    return AVAILABLE_SCRAPERS

def get_scrapers_for_role_type(role_type):
    """Get recommended scrapers for specific role types."""
    scraper_recommendations = {
        "entry_level": ["indeed", "ziprecruiter"],
        "senior_level": ["dice", "stackoverflow", "builtin"],
        "technical": ["dice", "stackoverflow"],
        "startup": ["builtin", "stackoverflow"],
        "enterprise": ["indeed", "dice"],
        "contract": ["dice", "ziprecruiter"],
        "remote": ["stackoverflow", "ziprecruiter", "builtin"],
        "all": list(AVAILABLE_SCRAPERS.keys())
    }
    return scraper_recommendations.get(role_type, scraper_recommendations["all"])

def get_search_scenario(scenario_name):
    """Get search configuration for a specific scenario."""
    return SEARCH_SCENARIOS.get(scenario_name, {})

def get_enhanced_configs():
    """Get enhanced search configurations for large-scale analysis."""
    return ENHANCED_SEARCH_CONFIGS

def get_working_configs():
    """Get working search configurations (proven successful)."""
    return WORKING_SEARCH_CONFIGS

def get_focused_configs():
    """Get focused test configurations for validation."""
    return FOCUSED_TEST_CONFIGS

def get_keywords_for_scenario(scenario_type="comprehensive"):
    """Get keywords list based on scenario type."""
    if scenario_type == "comprehensive":
        return ANALYTICS_JOB_TITLES
    elif scenario_type == "core":
        return SEARCH_SCENARIOS["core_analytics"]["titles"]
    elif scenario_type == "bi":
        return SEARCH_SCENARIOS["business_intelligence"]["titles"]
    elif scenario_type == "data_science":
        return SEARCH_SCENARIOS["data_science"]["titles"]
    elif scenario_type == "strategy":
        return SEARCH_SCENARIOS["strategy_operations"]["titles"]
    else:
        return ["Data Analyst", "Business Analyst"]  # Default fallback

if __name__ == "__main__":
    print("📊 Comprehensive Job Search Configuration")
    print("=" * 50)
    print(f"Total job titles configured: {len(ANALYTICS_JOB_TITLES)}")
    print(f"Search scenarios available: {len(SEARCH_SCENARIOS)}")
    print(f"Enhanced configurations: {len(ENHANCED_SEARCH_CONFIGS)}")
    print(f"Working configurations: {len(WORKING_SEARCH_CONFIGS)}")
    print(f"Focused test configurations: {len(FOCUSED_TEST_CONFIGS)}")
    
    print("\n🎯 All Analytics Job Titles:")
    for i, title in enumerate(ANALYTICS_JOB_TITLES, 1):
        print(f"  {i:2d}. {title}")
