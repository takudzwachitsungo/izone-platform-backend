from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Database - Use PostgreSQL for Vercel deployment
    database_url: str = "sqlite:///./izonedevs.db"  # Default for local dev
    
    # For Vercel, use environment variable
    @property
    def db_url(self):
        # Check for Vercel environment
        if os.getenv("VERCEL"):
            # Use in-memory SQLite for testing (data won't persist)
            return "sqlite:///:memory:"
        return self.database_url
    
    # Security
    secret_key: str = "your-secret-key-change-in-production-make-it-very-long-and-random"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # CORS - Updated for Vercel deployment
    allowed_origins: List[str] = [
        "http://localhost:8080", 
        "http://localhost:4000", 
        "http://localhost:3000", 
        "http://localhost:5173", 
        "http://127.0.0.1:8080", 
        "http://127.0.0.1:4000", 
        "http://127.0.0.1:3000", 
        "http://127.0.0.1:5173",
        "https://*.vercel.app",
        "https://yourdomain.com"
    ]
    
    # File uploads
    max_file_size: int = 10485760  # 10MB
    upload_dir: str = "uploads"
    
    # Email (Gmail SMTP)
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = "izonemakers@gmail.com"
    smtp_password: str = "kmub uxpm bhsw qnkd"
    
    # App settings
    debug: bool = True
    app_name: str = "iZonehub Makerspace API"
    app_version: str = "1.0.0"

    class Config:
        env_file = ".env"


settings = Settings()