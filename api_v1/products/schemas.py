from pydantic import BaseModel, ConfigDict, Field
from bson import ObjectId 
from datetime import datetime, timezone
from typing import Optional, Union

# Кастомный тип для ObjectId
class PyObjectId(ObjectId):
    """
    Кастомный тип для работы с ObjectId в Pydantic V2
    """
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return handler(ObjectId)
    
    @classmethod 
    def validate(cls, v):
        """Проверяем, что это валидный ObjectId"""
        if not ObjectId.is_valid(v):
            raise ValueError("Некорректный ObjectId")
        return ObjectId(v)

# Функция для получения текущего времени
def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)

# Базовые схемы
class ProductBase(BaseModel):
    name: str
    description: str
    price: float  # ← Изменил int на float (цена обычно дробная)

# Для создания
class ProductCreate(ProductBase):
    pass

# Для обновления (все поля опциональны)
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

# Частичное обновление (аналогично ProductUpdate)
class ProductUpdatePartial(ProductUpdate):
    pass

# SQL модель (если ещё используете)
class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: str

# MongoDB модель
class ProductInBd(ProductBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    
    # Pydantic V2 синтаксис
    model_config = ConfigDict(
        populate_by_name=True,        # замена allow_population_by_field_name
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        # Дополнительные настройки:
        str_strip_whitespace=True,
        validate_assignment=True,
    )

# Схема для ответа API (объединяет преимущества)
class ProductResponse(ProductBase):
    id: str  # Строковый ID для API
    
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )