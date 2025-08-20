def analyze_geographic_salary_differences(job_data):
    """
    Analyzes geographic salary differences and job availability from the provided job data.

    Parameters:
    job_data (DataFrame): A pandas DataFrame containing job postings with salary and location information.

    Returns:
    DataFrame: A DataFrame summarizing average salaries and job counts by geographic location.
    """
    import pandas as pd

    # Group by location and calculate average salary and job count
    geographic_analysis = job_data.groupby('location').agg(
        average_salary=('salary', 'mean'),
        job_count=('job_title', 'count')
    ).reset_index()

    return geographic_analysis


def visualize_geographic_analysis(geographic_data):
    """
    Visualizes the geographic salary analysis results using a bar chart.

    Parameters:
    geographic_data (DataFrame): A DataFrame containing the geographic analysis results.
    """
    import matplotlib.pyplot as plt

    plt.figure(figsize=(12, 6))
    plt.bar(geographic_data['location'], geographic_data['average_salary'], color='skyblue')
    plt.title('Average Salary by Geographic Location')
    plt.xlabel('Location')
    plt.ylabel('Average Salary')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()