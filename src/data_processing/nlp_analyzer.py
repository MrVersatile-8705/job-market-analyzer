from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np

class NLPAnalyzer:
    def __init__(self, job_descriptions):
        self.job_descriptions = job_descriptions
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.model = None

    def preprocess_data(self):
        # Convert job descriptions to lowercase
        self.job_descriptions = [desc.lower() for desc in self.job_descriptions]

    def vectorize_data(self):
        # Vectorize job descriptions using TF-IDF
        self.tfidf_matrix = self.vectorizer.fit_transform(self.job_descriptions)

    def cluster_data(self, num_clusters):
        # Perform KMeans clustering on the TF-IDF matrix
        self.model = KMeans(n_clusters=num_clusters, random_state=42)
        self.model.fit(self.tfidf_matrix)

    def get_clustered_data(self):
        # Get the cluster labels for each job description
        return self.model.labels_

    def get_top_keywords(self, num_keywords=5):
        # Get top keywords for each cluster
        order_centroids = self.model.cluster_centers_.argsort()[:, ::-1]
        terms = self.vectorizer.get_feature_names_out()
        top_keywords = {}
        for i in range(self.model.n_clusters):
            top_keywords[i] = [terms[ind] for ind in order_centroids[i, :num_keywords]]
        return top_keywords

    def analyze(self, num_clusters):
        self.preprocess_data()
        self.vectorize_data()
        self.cluster_data(num_clusters)
        return self.get_top_keywords()