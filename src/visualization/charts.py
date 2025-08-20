from matplotlib import pyplot as plt
import pandas as pd

def plot_skill_distribution(skill_data):
    """
    Plots the distribution of skills from the provided skill data.

    Parameters:
    skill_data (pd.DataFrame): A DataFrame containing skill names and their frequencies.
    """
    plt.figure(figsize=(12, 6))
    plt.bar(skill_data['skill'], skill_data['frequency'], color='skyblue')
    plt.title('Skill Distribution in Job Descriptions')
    plt.xlabel('Skills')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_salary_distribution(salary_data):
    """
    Plots the distribution of salaries from the provided salary data.

    Parameters:
    salary_data (pd.DataFrame): A DataFrame containing salary ranges and their frequencies.
    """
    plt.figure(figsize=(12, 6))
    plt.hist(salary_data['salary'], bins=30, color='lightgreen', edgecolor='black')
    plt.title('Salary Distribution of Job Postings')
    plt.xlabel('Salary')
    plt.ylabel('Number of Job Postings')
    plt.tight_layout()
    plt.show()

def plot_experience_requirements(experience_data):
    """
    Plots the experience requirements for different job roles.

    Parameters:
    experience_data (pd.DataFrame): A DataFrame containing job roles and their experience requirements.
    """
    plt.figure(figsize=(12, 6))
    plt.bar(experience_data['job_role'], experience_data['experience_years'], color='salmon')
    plt.title('Experience Requirements by Job Role')
    plt.xlabel('Job Role')
    plt.ylabel('Years of Experience Required')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()