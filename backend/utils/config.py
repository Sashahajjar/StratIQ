"""
Configuration and environment settings
"""

import os
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/stratiq")
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Groq (Free AI alternative)
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    # External APIs
    NEWS_API_KEY: str = os.getenv("NEWS_API_KEY", "")
    CRUNCHBASE_API_KEY: str = os.getenv("CRUNCHBASE_API_KEY", "")
    
    # RapidAPI
    RAPIDAPI_KEY: str = os.getenv("RAPIDAPI_KEY", "")
    RAPIDAPI_HOST: str = os.getenv("RAPIDAPI_HOST", "")
    ALPHA_VANTAGE_HOST: str = os.getenv("ALPHA_VANTAGE_HOST", "alpha-vantage.p.rapidapi.com")
    YAHOO_FINANCE_HOST: str = os.getenv("YAHOO_FINANCE_HOST", "yahoo-finance15.p.rapidapi.com")
    CRUNCHBASE_HOST: str = os.getenv("CRUNCHBASE_HOST", "crunchbase-crunchbase-com.p.rapidapi.com")
    
    # CORS
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "http://localhost:3000")
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

