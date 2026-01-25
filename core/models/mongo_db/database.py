from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
from core.config import settings

class MongoDB:
    client:Optional[AsyncIOMotorClient] = None
    database : Optional[AsyncIOMotorDatabase] = None


    @classmethod
    async def connect(cls):
        try:
            cls.client  = AsyncIOMotorClient(settings.mongodb_url)
            await cls.client.admin.command('ping')

            cls.database = cls.client[settings.mongo_database]

            print("MongoDB подключен")

        except Exception as e:
            print(f"Ошибка подключения: {e}")
            raise

    @classmethod
    async def disconnect(cls):
        """Закрываем подключение при остановке приложения"""
        if cls.client:
            cls.client.close()
            print("MongoDB отключен")

    @classmethod
    def get_database(cls):
        """
        Возвращает объект базы данных
        Используется в CRUD операциях
        """
        if cls.database is None:
            raise RuntimeError("MongoDB не подключен!")
        return cls.database

mongodb = MongoDB()