def validate_data(job_data_list):
    """
    Validates a list of job data entries - alias for validate_job_data_list.
    This function is used by main.py for data validation.

    Parameters:
    job_data_list (list): A list of dictionaries containing job data to validate.

    Returns:
    list: A list of valid job data entries.
    """
    return validate_job_data_list(job_data_list)


def validate_job_data(job_data):
    """
    Validates the scraped job data to ensure it meets quality standards.

    Parameters:
    job_data (dict): A dictionary containing job data to validate.

    Returns:
    bool: True if the job data is valid, False otherwise.
    """
    required_fields = ['title', 'company', 'location', 'description', 'salary']
    
    for field in required_fields:
        if field not in job_data or not job_data[field]:
            return False
    
    # Additional validation rules can be added here
    return True


def validate_job_data_list(job_data_list):
    """
    Validates a list of job data entries.

    Parameters:
    job_data_list (list): A list of dictionaries containing job data to validate.

    Returns:
    list: A list of valid job data entries.
    """
    valid_jobs = []
    
    for job in job_data_list:
        if validate_job_data(job):
            valid_jobs.append(job)
    
    return valid_jobs