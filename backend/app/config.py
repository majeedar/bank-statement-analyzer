from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    environment: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ]
    
    class Config:
        env_file = ".env"

settings = Settings()
