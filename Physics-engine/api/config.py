# api/config.py
import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """API configuration"""
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS
    ALLOWED_ORIGINS: list = ["*"]
    
    # Simulation defaults
    DEFAULT_DT: float = 3600.0
    DEFAULT_INTEGRATOR: str = "verlet"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()