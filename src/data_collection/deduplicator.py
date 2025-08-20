def remove_duplicates(job_postings):
    """
    Remove duplicate job postings from the dataset.

    Parameters:
    job_postings (list of dict): A list of job postings where each posting is represented as a dictionary.

    Returns:
    list of dict: A list of unique job postings.
    """
    unique_postings = []
    seen_titles = set()

    for posting in job_postings:
        title = posting.get('title')
        if title not in seen_titles:
            seen_titles.add(title)
            unique_postings.append(posting)

    return unique_postings


def deduplicate_job_data(input_file, output_file):
    """
    Read job postings from a file, remove duplicates, and write the unique postings to a new file.

    Parameters:
    input_file (str): The path to the input file containing job postings.
    output_file (str): The path to the output file where unique postings will be saved.
    """
    import json

    with open(input_file, 'r') as infile:
        job_postings = json.load(infile)

    unique_postings = remove_duplicates(job_postings)

    with open(output_file, 'w') as outfile:
        json.dump(unique_postings, outfile, indent=4)