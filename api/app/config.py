# api/app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """API configuration"""
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    ALLOWED_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()