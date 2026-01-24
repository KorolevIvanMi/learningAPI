from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from bson import ObjectId
from typing import List, Optional, Dict

from .schemas import  Product, ProductResponse 

from .crud import ProductCRUD, get_product_crud


async def get_product_by_id(
    product_id: Annotated[str, Path], 
    crud: ProductCRUD = Depends(get_product_crud)
) -> ProductResponse:  # ← Возвращаем Pydantic модель, а не Dict!
    
    # Проверяем валидность ObjectId
    if not ObjectId.is_valid(product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,  # 400 вместо 404 для невалидного ID
            detail=f"Invalid product ID format: {product_id}"
        )
    
    # Получаем продукт из MongoDB
    product_dict = await crud.get(product_id)
    
    if not product_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {product_id} not found!"
        )
    
    # Конвертируем Dict в Pydantic модель
    return ProductResponse(**product_dict)


