import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_secret(key: str, default: str = '') -> str:
    """Get a secret from Streamlit secrets or environment variables."""
    try:
        import streamlit as st
        # Try to get from Streamlit secrets first
        if hasattr(st, 'secrets') and st.secrets:
            return st.secrets.get(key, default)
    except:
        pass
    
    # Fallback to environment variables
    return os.getenv(key, default)

class Config:
    """Configuration management for the violation detection system."""
    
    # HuggingFace API Configuration
    HUGGINGFACE_API_TOKEN = get_secret('HUGGINGFACE_API_TOKEN', '')
    
    # Email Configuration
    EMAIL_HOST = get_secret('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
    EMAIL_PORT = int(get_secret('EMAIL_SMTP_PORT', '587'))
    EMAIL_USER = get_secret('EMAIL_SENDER_EMAIL', '')
    EMAIL_PASSWORD = get_secret('EMAIL_SENDER_PASSWORD', '')
    RESIDENCE_LIFE_EMAIL = get_secret('EMAIL_RESIDENCE_LIFE_EMAIL', 'residencelife@university.edu')
    
    # Model Configuration
    CLIP_MODEL_NAME = "openai/clip-vit-base-patch32"
    LLM_MODEL_NAME = "microsoft/DialoGPT-medium"
    
    # File Upload Configuration
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.pdf'}
    
    # Database Configuration
    CHROMA_DB_PATH = "chroma_db"
    
    # Report Configuration
    REPORTS_DIR = "reports"
    
    # Validation Configuration
    MIN_CONFIDENCE_THRESHOLD = 0.3
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that all required configuration is present."""
        if not cls.HUGGINGFACE_API_TOKEN:
            raise ValueError("HUGGINGFACE_API_TOKEN must be set")
        
        # Create necessary directories
        os.makedirs(cls.REPORTS_DIR, exist_ok=True)
        os.makedirs(cls.CHROMA_DB_PATH, exist_ok=True)
        
        return True
    
    @classmethod
    def get_report_path(cls, filename: str) -> str:
        """Get the full path for a report file."""
        return os.path.join(cls.REPORTS_DIR, filename)

# Global config instance
config = Config() 