def analyze_salary_trends(job_data):
    """
    Analyzes salary trends based on job postings.

    Parameters:
    job_data (DataFrame): A pandas DataFrame containing job postings with salary information.

    Returns:
    DataFrame: A DataFrame containing salary trends over time.
    """
    import pandas as pd

    # Ensure the 'salary' column is numeric
    job_data['salary'] = pd.to_numeric(job_data['salary'], errors='coerce')

    # Group by year and calculate average salary
    job_data['year'] = job_data['date_posted'].dt.year
    salary_trends = job_data.groupby('year')['salary'].mean().reset_index()

    return salary_trends


def compare_salary_by_role(job_data):
    """
    Compares average salaries by job role.

    Parameters:
    job_data (DataFrame): A pandas DataFrame containing job postings with role and salary information.

    Returns:
    DataFrame: A DataFrame containing average salaries by job role.
    """
    import pandas as pd

    # Ensure the 'salary' column is numeric
    job_data['salary'] = pd.to_numeric(job_data['salary'], errors='coerce')

    # Group by job role and calculate average salary
    salary_by_role = job_data.groupby('job_role')['salary'].mean().reset_index()

    return salary_by_role


def salary_distribution(job_data):
    """
    Analyzes the distribution of salaries in the job postings.

    Parameters:
    job_data (DataFrame): A pandas DataFrame containing job postings with salary information.

    Returns:
    dict: A dictionary containing statistics about salary distribution.
    """
    import pandas as pd

    # Ensure the 'salary' column is numeric
    job_data['salary'] = pd.to_numeric(job_data['salary'], errors='coerce')

    # Calculate statistics
    salary_stats = {
        'mean': job_data['salary'].mean(),
        'median': job_data['salary'].median(),
        'min': job_data['salary'].min(),
        'max': job_data['salary'].max(),
        'std_dev': job_data['salary'].std()
    }

    return salary_stats