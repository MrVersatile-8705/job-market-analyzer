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
    # Normalize text by cleaning and removing stop words
    from nltk.corpus import stopwords
    
    stop_words = set(stopwords.words('english'))
    words = text.split()
    normalized_text = ' '.join(word for word in words if word not in stop_words)
    
    return normalized_text

def process_job_description(job_description):
    # Clean and normalize the job description
    cleaned_text = clean_text(job_description)
    normalized_text = normalize_text(cleaned_text)
    
    return normalized_text