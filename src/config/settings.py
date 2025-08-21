import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings and configuration."""
    
    def __init__(self):
        # Database settings
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///data/job_market_dev.db")
        self.database_url_dev = os.getenv("DATABASE_URL_DEV", "sqlite:///data/job_market_dev.db")
        
        # API Keys
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
        self.ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")  # Legacy support
        
        # Scraping settings
        self.scraping_delay_min = int(os.getenv("SCRAPING_DELAY_MIN", "1"))
        self.scraping_delay_max = int(os.getenv("SCRAPING_DELAY_MAX", "3"))
        self.max_retries = int(os.getenv("MAX_RETRIES", "3"))
        self.use_proxy = os.getenv("USE_PROXY", "false").lower() == "true"
        
        # Application settings
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.debug_mode = os.getenv("DEBUG_MODE", "true").lower() == "true"
        self.max_workers = int(os.getenv("MAX_WORKERS", "4"))
        
        # Rate limiting
        self.requests_per_minute = int(os.getenv("REQUESTS_PER_MINUTE", "30"))
        self.linkedin_rate_limit = int(os.getenv("LINKEDIN_RATE_LIMIT", "10"))
        self.indeed_rate_limit = int(os.getenv("INDEED_RATE_LIMIT", "20"))
        self.glassdoor_rate_limit = int(os.getenv("GLASSDOOR_RATE_LIMIT", "15"))
        
        # Project paths
        self.project_root = Path(__file__).parent.parent.parent
        self.data_dir = self.project_root / "data"
        self.logs_dir = self.project_root / "logs"
        
        # Create directories if they don't exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        (self.data_dir / "raw").mkdir(parents=True, exist_ok=True)
        (self.data_dir / "processed").mkdir(parents=True, exist_ok=True)
        (self.data_dir / "results").mkdir(parents=True, exist_ok=True)

# Global settings instance
settings = Settings()