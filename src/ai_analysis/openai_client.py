from openai import OpenAI

class OpenAIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)

    def analyze_job_description(self, job_description):
        response = self.client.Completion.create(
            engine="text-davinci-003",
            prompt=f"Analyze the following job description and extract key skills, requirements, and compensation patterns:\n\n{job_description}",
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].text.strip()

    def extract_skills(self, job_description):
        response = self.client.Completion.create(
            engine="text-davinci-003",
            prompt=f"Extract the skills required from the following job description:\n\n{job_description}",
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].text.strip().split(', ')

    def categorize_requirements(self, job_description):
        response = self.client.Completion.create(
            engine="text-davinci-003",
            prompt=f"Categorize the requirements from the following job description:\n\n{job_description}",
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].text.strip()