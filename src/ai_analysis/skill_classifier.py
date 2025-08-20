from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import re

class SkillClassifier(BaseEstimator, TransformerMixin):
    def __init__(self, skill_keywords):
        self.skill_keywords = skill_keywords

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.apply(self._classify_skills)

    def _classify_skills(self, job_description):
        found_skills = []
        for skill, keywords in self.skill_keywords.items():
            if any(re.search(r'\b' + re.escape(keyword) + r'\b', job_description, re.IGNORECASE) for keyword in keywords):
                found_skills.append(skill)
        return found_skills

# Example usage:
# skill_keywords = {
#     'Python': ['python', 'pandas', 'numpy'],
#     'SQL': ['sql', 'postgresql', 'mysql'],
#     'Machine Learning': ['machine learning', 'ml', 'deep learning'],
#     'Data Visualization': ['tableau', 'power bi', 'matplotlib'],
# }
# classifier = SkillClassifier(skill_keywords)
# job_descriptions = pd.Series(["Looking for a data analyst with experience in Python and SQL."])
# classified_skills = classifier.fit_transform(job_descriptions)
# print(classified_skills)