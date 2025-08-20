import sys
from pathlib import Path
from loguru import logger
from .settings import settings

def setup_logging():
    """Configure logging for the application."""
    
    # Remove default handler
    logger.remove()
    
    # Console handler
    logger.add(
        sys.stdout,
        level=settings.log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True
    )
    
    # File handler for all logs
    logger.add(
        settings.logs_dir / "app.log",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="100 MB",
        retention="30 days",
        compression="zip"
    )
    
    # Separate file for errors
    logger.add(
        settings.logs_dir / "errors.log",
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="50 MB",
        retention="90 days",
        compression="zip"
    )
    
    # Scraping specific logs
    logger.add(
        settings.logs_dir / "scraping.log",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        filter=lambda record: "scraper" in record["name"].lower(),
        rotation="50 MB",
        retention="30 days"
    )
    
    return logger

# Initialize logging
setup_logging()
