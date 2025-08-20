def categorize_requirements(job_descriptions):
    """
    Categorizes job requirements from a list of job descriptions.

    Args:
        job_descriptions (list of str): A list of job descriptions.

    Returns:
        dict: A dictionary with categories as keys and lists of requirements as values.
    """
    categories = {
        'Technical Skills': [],
        'Soft Skills': [],
        'Experience': [],
        'Education': [],
        'Certifications': []
    }

    # Example keywords for categorization
    technical_keywords = ['Python', 'SQL', 'Java', 'R', 'AWS', 'Azure', 'Machine Learning', 'Data Analysis']
    soft_keywords = ['communication', 'teamwork', 'problem-solving', 'leadership', 'adaptability']
    experience_keywords = ['years of experience', 'entry-level', 'senior', 'junior']
    education_keywords = ['Bachelor', 'Master', 'PhD', 'degree']
    certification_keywords = ['Certified', 'Certification', 'AWS Certified', 'Google Certified']

    for description in job_descriptions:
        for keyword in technical_keywords:
            if keyword.lower() in description.lower():
                categories['Technical Skills'].append(keyword)

        for keyword in soft_keywords:
            if keyword.lower() in description.lower():
                categories['Soft Skills'].append(keyword)

        for keyword in experience_keywords:
            if keyword.lower() in description.lower():
                categories['Experience'].append(keyword)

        for keyword in education_keywords:
            if keyword.lower() in description.lower():
                categories['Education'].append(keyword)

        for keyword in certification_keywords:
            if keyword.lower() in description.lower():
                categories['Certifications'].append(keyword)

    # Remove duplicates from each category
    for key in categories:
        categories[key] = list(set(categories[key]))

    return categories


def main():
    # Example job descriptions
    job_descriptions = [
        "Looking for a Data Analyst with 2+ years of experience in Python and SQL.",
        "Seeking a Machine Learning Engineer with strong communication skills and a Master's degree.",
        "Entry-level position available for a Data Scientist with AWS certification."
    ]

    categorized_requirements = categorize_requirements(job_descriptions)
    print(categorized_requirements)


if __name__ == "__main__":
    main()