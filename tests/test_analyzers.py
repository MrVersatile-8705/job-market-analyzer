import pytest
from src.statistical_analysis.salary_analyzer import analyze_salary_trends
from src.statistical_analysis.correlation_analyzer import analyze_correlations
from src.ai_analysis.skill_classifier import classify_skills
from src.ai_analysis.requirement_categorizer import categorize_requirements

def test_analyze_salary_trends():
    # Sample data for testing
    sample_data = [
        {'job_title': 'Data Analyst', 'salary': 70000, 'location': 'New York'},
        {'job_title': 'Data Scientist', 'salary': 120000, 'location': 'San Francisco'},
        {'job_title': 'ML Engineer', 'salary': 150000, 'location': 'Austin'},
    ]
    result = analyze_salary_trends(sample_data)
    assert isinstance(result, dict)
    assert 'average_salary' in result
    assert result['average_salary'] > 0

def test_analyze_correlations():
    # Sample data for testing
    sample_data = [
        {'job_title': 'Data Analyst', 'salary': 70000, 'experience': 2},
        {'job_title': 'Data Scientist', 'salary': 120000, 'experience': 5},
        {'job_title': 'ML Engineer', 'salary': 150000, 'experience': 4},
    ]
    result = analyze_correlations(sample_data)
    assert isinstance(result, dict)
    assert 'correlation_coefficient' in result
    assert -1 <= result['correlation_coefficient'] <= 1

def test_classify_skills():
    # Sample skills for testing
    sample_skills = ['Python', 'SQL', 'Machine Learning']
    result = classify_skills(sample_skills)
    assert isinstance(result, list)
    assert len(result) == len(sample_skills)

def test_categorize_requirements():
    # Sample requirements for testing
    sample_requirements = ['3+ years of experience in Python', 'Strong SQL skills', 'Experience with AWS']
    result = categorize_requirements(sample_requirements)
    assert isinstance(result, dict)
    assert 'technical' in result
    assert 'soft' in result