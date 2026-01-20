try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class AIConfig(BaseSettings):
    """
    Configuration class for AI API settings (Google Gemini)
    """
    api_key: str = os.getenv("GEMINI_API_KEY", "")
    model: str = os.getenv("GEMINI_MODEL", "gemini-pro")
    temperature: float = 0.7
    max_tokens: int = 1000
    timeout: int = 30

    model_config = {"env_prefix": "gemini_"}

# Global instance
ai_config = AIConfig()