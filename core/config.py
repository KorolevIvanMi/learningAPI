from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DATABASE: str = os.getenv("MONGODB_DATABASE", "my_shop")
    
    api_v1_prefix: str = "/api/v1"
    # db_url: str = "sqlite+aiosqlite:///./shop.db"

settings = Settings()

