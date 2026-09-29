import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    Application settings and environment variable validation.
    """
    # App Settings
    APP_NAME: str = "QualifAI"
    DEBUG: bool = False
    
    # Brain Settings
    OPENAI_API_KEY: str
    MODEL_NAME: str = "gpt-4o"
    
    # Company Info (White-label ready)
    COMPANY_NAME: str = "QualifAI Systems"
    COMPANY_DESCRIPTION: str = "AI-powered lead qualification and appointment booking."
    BOOKING_LINK: str = "https://calendly.com/example"
    
    # Gmail Integration
    GMAIL_USER: Optional[str] = None
    GMAIL_PASSWORD: Optional[str] = None # App Password
    
    # Twilio Integration
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE_NUMBER: Optional[str] = None
    
    # Calendar Integration (Google)
    GOOGLE_CALENDAR_ID: str = "primary"
    
    # Webhook Settings
    WEBHOOK_PORT: int = 8080
    WEBHOOK_HOST: str = "0.0.0.0"
    WEBHOOK_SECRET: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
