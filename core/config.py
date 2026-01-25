import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pydantic import model_validator

# Загружаем переменные из .env файла
load_dotenv()

class Settings(BaseSettings):
    # Настройки приложения
    app_name: str = "FastAPI Products API"
    
    # Префикс для API v1
    api_v1_prefix: str = "/api/v1"
    
    # Настройки MongoDB из переменных окружения
    mongo_app_user: str = os.getenv("MONGO_APP_USER", "app_user")
    mongo_app_password: str = os.getenv("MONGO_APP_PASSWORD", "123")
    mongo_database: str = os.getenv("MONGO_DATABASE", "products_db")
    
    mongodb_url: str = ""  # Объявляем поле

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Вычисляем URL после инициализации
        self.mongodb_url = (
        f"mongodb://{self.mongo_app_user}:{self.mongo_app_password}"
        f"@mongodb:27017/{self.mongo_database}"
        f"?authSource={self.mongo_database}"
)

# Создаем экземпляр настроек
settings = Settings()