from typing import Any, Dict
import requests

class ClaudeClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.claude.ai/v1"

    def analyze_text(self, text: str) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "text": text
        }
        response = requests.post(f"{self.base_url}/analyze", headers=headers, json=payload)
        
        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code} - {response.text}")
        
        return response.json()

    def extract_skills(self, job_description: str) -> Dict[str, Any]:
        analysis_result = self.analyze_text(job_description)
        return analysis_result.get("skills", [])

    def categorize_requirements(self, job_description: str) -> Dict[str, Any]:
        analysis_result = self.analyze_text(job_description)
        return analysis_result.get("requirements", {})