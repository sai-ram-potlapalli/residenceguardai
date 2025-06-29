import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration management for the violation detection system."""
    
    # HuggingFace API Configuration
    HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN', '')
    
    # Email Configuration
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
    EMAIL_USER = os.getenv('EMAIL_USER', '')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    RESIDENCE_LIFE_EMAIL = os.getenv('RESIDENCE_LIFE_EMAIL', 'residencelife@university.edu')
    
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

# Global config instance
config = Config() 