


from typing import List, Optional, Dict
from bson import ObjectId
from datetime import datetime, timezone

from core.models.mongo_db.database import mongodb
from .schemas import ProductCreate, ProductUpdate, ProductUpdatePartial


class ProductCRUD:
    def __init__(self):
        self.collection  = mongodb.get_database().products


    async def create_product(self, product_in: ProductCreate)->Dict:
        product_dict = product_in.model_dump()

        product_dict["created_at"] = datetime.now(timezone.utc)
        product_dict["updated_at"] = datetime.now(timezone.utc)

        result = await self.collection.insert_one(product_dict)

        created = await self.collection.find_one({"_id": result.inserted_id})
        
        created["id"] = str(created["_id"])
        del created["_id"]
        
        return created


    async def get(self, product_id: str) -> Optional[Dict]:
        """
        ПОЛУЧЕНИЕ продукта по ID
        SELECT ... WHERE id = ? → find_one({"_id": ObjectId(id)})
        """
        # Проверяем, что это валидный ObjectId
        if not ObjectId.is_valid(product_id):
            return None
        
        # Ищем документ по _id
        product = await self.collection.find_one({"_id": ObjectId(product_id)})
        
        if product:
            # Конвертируем для API
            product["id"] = str(product["_id"])
            del product["_id"]
        
        return product
    

    async def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Dict]:
        """
        ПОЛУЧЕНИЕ ВСЕХ продуктов
        SELECT * FROM products → find()
        """
        # Получаем курсор (ленивая загрузка)
        cursor = self.collection.find().skip(skip).limit(limit)
        
        # Преобразуем в список
        products = await cursor.to_list(length=limit)
        
        # Конвертируем ObjectId для каждого документа
        for product in products:
            product["id"] = str(product["_id"])
            del product["_id"]
        
        return products
    

    async def update(
        self, 
        product_id: str, 
        product_update: ProductUpdate
    ) -> Optional[Dict]:
        """
        ОБНОВЛЕНИЕ продукта
        UPDATE ... SET ... WHERE id = ? → update_one({"_id": ObjectId(id)}, {"$set": {...}})
        """
        if not ObjectId.is_valid(product_id):
            return None
        
        # Удаляем None значения из обновления
        update_data = product_update.dict(exclude_none=True)
        
        # Добавляем время обновления
        update_data["updated_at"] = datetime.utcnow()
        
        # Выполняем обновление
        result = await self.collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": update_data}
        )
        
        # Если документ обновлен, возвращаем обновленную версию
        if result.modified_count > 0:
            return await self.get(product_id)
        
        return None
    
    async def delete(self, product_id: str) -> bool:
        """
        УДАЛЕНИЕ продукта  
        DELETE FROM ... WHERE id = ? → delete_one({"_id": ObjectId(id)})
        """
        if not ObjectId.is_valid(product_id):
            return False
        
        result = await self.collection.delete_one({"_id": ObjectId(product_id)})
        
        # deleted_count > 0 означает, что документ был удален
        return result.deleted_count > 0
    

def get_product_crud() -> ProductCRUD:
    """Фабрика для получения CRUD (используется в Depends)"""
    return ProductCRUD()