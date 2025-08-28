"""
Configuration settings for Marie Knowledge System
"""

from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Marie Knowledge System"
    VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # API
    API_V1_STR: str = "/api/v1"
    
    # CORS
    ALLOWED_HOSTS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]
    
    # Database
    DATABASE_URL: str = "sqlite:///./marie.db"
    
    # Vector Database
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"
    CHROMA_COLLECTION_NAME: str = "marie_knowledge"
    
    # AI Models
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    LIGHTWEIGHT_MODEL: str = "llama3.2:3b"
    DEEP_MODEL: str = "llama3.1:8b"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # File Storage
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    
    # Content Processing
    YOUTUBE_API_KEY: str = ""  # Optional, for enhanced metadata
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Ensure directories exist
Path(settings.UPLOAD_DIR).mkdir(exist_ok=True)
Path(settings.CHROMA_PERSIST_DIRECTORY).mkdir(exist_ok=True)
