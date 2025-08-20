import pytest
from src.data_processing.text_processor import clean_text, normalize_text
from src.data_processing.skill_extractor import extract_skills
from src.data_processing.salary_parser import parse_salary
from src.data_processing.nlp_analyzer import analyze_nlp

def test_clean_text():
    assert clean_text("This is a TEST!") == "this is a test"
    assert clean_text("   Extra spaces   ") == "extra spaces"
    assert clean_text("Special characters #$%^&*()") == "special characters"

def test_normalize_text():
    assert normalize_text("Data Science") == "data science"
    assert normalize_text("Machine Learning") == "machine learning"

def test_extract_skills():
    job_description = "We are looking for a data analyst with skills in Python, SQL, and Tableau."
    expected_skills = {"Python", "SQL", "Tableau"}
    assert extract_skills(job_description) == expected_skills

def test_parse_salary():
    assert parse_salary("Salary: $80,000 - $100,000") == (80000, 100000)
    assert parse_salary("Annual Salary: $120,000") == (120000, 120000)
    assert parse_salary("Compensation: $70K") == (70000, 70000)

def test_analyze_nlp():
    job_description = "Looking for a data scientist with experience in Python and machine learning."
    analysis_result = analyze_nlp(job_description)
    assert "data scientist" in analysis_result['roles']
    assert "Python" in analysis_result['skills']