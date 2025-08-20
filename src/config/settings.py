# settings.py

import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data directories
RAW_DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw')
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')
RESULTS_DIR = os.path.join(BASE_DIR, 'data', 'results')

# API settings
API_TIMEOUT = 30  # seconds
MAX_RETRIES = 5

# Logging settings
LOGGING_LEVEL = 'INFO'
LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# NLP settings
NLP_MODEL = 'en_core_web_sm'  # Default NLP model to use

# Cloud settings
CLOUD_PROVIDER = 'AWS'  # Default cloud provider
CLOUD_REGION = 'us-east-1'  # Default region for cloud services

# Other configurations
ENABLE_CACHING = True
CACHE_DIR = os.path.join(BASE_DIR, 'cache')