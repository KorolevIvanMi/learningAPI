from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.models.mongo_db.database import mongodb
from core.config import settings
from api_v1 import router as router_v1
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Запуск - подключаемся к MongoDB
    await mongodb.connect()
    
    yield  # Приложение работает
    
    # Остановка - отключаемся от MongoDB
    await mongodb.disconnect()

# Создаем приложение
app = FastAPI(lifespan=lifespan)

# Подключаем роутер API
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)

# Простой endpoint для проверки
@app.get("/")
def hello_index():
    return {"message": "FastAPI with MongoDB is running"}

@app.get("/health")
async def health_check():
    try:
        # Проверяем что MongoDB доступна
        await mongodb.client.admin.command('ping')
        return {"status": "healthy", "database": "connected"}
    except Exception:
        return {"status": "unhealthy", "database": "disconnected"}
    
uvicorn.run(
        "main:app",
        host="127.0.0.1",  # или "0.0.0.0" для доступа из сети
        port=8000)