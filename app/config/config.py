"""
Application configuration settings
Loads environment variables and provides configuration constants
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# AWS Configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")

# AI Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# Bidding API Configuration
BIDDING_API_BASE_URL = os.getenv("BIDDING_API_BASE_URL", "http://localhost:8080")
BIDDING_API_TIMEOUT = int(os.getenv("BIDDING_API_TIMEOUT", "30"))

# Available LLM Models
LLM_MODELS = {
    "gemma": "google/gemma-3n-e4b-it:free",
    "deepseek": "tngtech/deepseek-r1t2-chimera:free", 
    "dolphin": "cognitivecomputations/dolphin3.0-r1-mistral-24b:free"
}

# Default model
DEFAULT_LLM_MODEL = "dolphin"

# Application Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
MAX_MESSAGES_PER_POLL = int(os.getenv("MAX_MESSAGES_PER_POLL", "1"))
POLL_WAIT_TIME = int(os.getenv("POLL_WAIT_TIME", "10"))

# Validation
def validate_config():
    """Validate required configuration variables"""
    required_vars = [
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY", 
        "SQS_QUEUE_URL",
        "AWS_S3_BUCKET",
        "OPENROUTER_API_KEY",
        "BIDDING_API_BASE_URL",
        "BIDDING_API_TIMEOUT",
    ]
    
    missing_vars = []
    for var in required_vars:
        if not globals().get(var):
            missing_vars.append(var)
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Validate configuration on import
validate_config()
