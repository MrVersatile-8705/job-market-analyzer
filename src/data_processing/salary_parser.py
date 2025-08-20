def parse_salary(job_description):
    import re

    # Regular expression patterns for salary extraction
    salary_patterns = [
        r'\$\d{1,3}(?:,\d{3})*(?:\s*-\s*\$\d{1,3}(?:,\d{3})*)?',  # e.g., $50,000 - $70,000
        r'\$\d{1,3}(?:,\d{3})*',  # e.g., $50,000
        r'\d{1,3}(?:,\d{3})*\s*per\s*year',  # e.g., 50,000 per year
        r'\$\d{1,3}(?:,\d{3})*\s*hour',  # e.g., $25/hour
        r'\$\d{1,3}(?:,\d{3})*\s*monthly'  # e.g., $4,000 monthly
    ]

    salaries = []
    for pattern in salary_patterns:
        matches = re.findall(pattern, job_description)
        salaries.extend(matches)

    return salaries

def extract_salary_range(salary_string):
    # Extracts the minimum and maximum salary from a salary range string
    salary_range_pattern = r'\$(\d{1,3}(?:,\d{3})*)\s*-\s*\$(\d{1,3}(?:,\d{3})*)'
    match = re.search(salary_range_pattern, salary_string)
    if match:
        min_salary = int(match.group(1).replace(',', ''))
        max_salary = int(match.group(2).replace(',', ''))
        return min_salary, max_salary
    return None

def convert_salary_to_float(salary_string):
    # Converts a salary string to a float value
    salary_string = salary_string.replace('$', '').replace(',', '').strip()
    return float(salary_string) if salary_string else None

def analyze_salaries(job_descriptions):
    salary_data = []
    for description in job_descriptions:
        salaries = parse_salary(description)
        for salary in salaries:
            if '-' in salary:
                salary_range = extract_salary_range(salary)
                if salary_range:
                    salary_data.append({
                        'min_salary': salary_range[0],
                        'max_salary': salary_range[1]
                    })
            else:
                salary_value = convert_salary_to_float(salary)
                if salary_value is not None:
                    salary_data.append({
                        'min_salary': salary_value,
                        'max_salary': salary_value
                    })
    return salary_data