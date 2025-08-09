from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "ReHumanizer"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_SECRET: str = "your-jwt-secret-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/rehumanizer"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://rehumanizer.com"
    ]
    
    # File upload
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    UPLOAD_DIR: str = "uploads"
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_DAY: int = 1000
    
    # Humanization settings
    MAX_TEXT_LENGTH: int = 10000
    PROCESSING_TIMEOUT: int = 30  # seconds
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 