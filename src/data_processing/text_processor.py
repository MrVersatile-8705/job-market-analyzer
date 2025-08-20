def clean_text(text):
    import re
    
    # Remove HTML tags
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)
    
    # Remove non-alphanumeric characters (except for spaces)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def normalize_text(text):
    # Normalize text by cleaning and removing common stop words
    # Using a simple list instead of nltk to avoid dependencies
    
    simple_stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 
        'with', 'by', 'as', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 
        'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'
    }
    
    words = text.split()
    normalized_text = ' '.join(word for word in words if word.lower() not in simple_stop_words)
    
    return normalized_text

def process_text(job_data_list):
    """
    Process a list of job data by cleaning and normalizing text fields.
    
    Args:
        job_data_list (list): List of job dictionaries
        
    Returns:
        list: List of processed job dictionaries
    """
    processed_jobs = []
    
    for job in job_data_list:
        processed_job = job.copy()
        
        # Process description field if it exists
        if 'description' in job and job['description']:
            processed_job['description'] = process_job_description(job['description'])
        
        # Process title field
        if 'title' in job and job['title']:
            processed_job['title'] = clean_text(job['title'])
            
        # Process summary field if it exists (for Indeed scraper)
        if 'summary' in job and job['summary']:
            processed_job['summary'] = process_job_description(job['summary'])
            
        processed_jobs.append(processed_job)
    
    return processed_jobs


def process_job_description(job_description):
    # Clean and normalize the job description
    cleaned_text = clean_text(job_description)
    normalized_text = normalize_text(cleaned_text)
    
    return normalized_text