from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from .crud import ProductCRUD, get_product_crud

from .schemas import Product, ProductCreate, ProductUpdate, ProductUpdatePartial
from .dependencies import get_product_by_id

router = APIRouter(tags=["Products"])

@router.get("/", response_model=List[Product])
async def get_products(
    skip: int = 0,
    limit: int = 100,
    product_crud: ProductCRUD = Depends(get_product_crud),
):
    """Получение всех продуктов - теперь из MongoDB"""
    return await product_crud.get_all(skip=skip, limit=limit)


@router.post("/", response_model=ProductCreate, status_code= status.HTTP_201_CREATED,)
async def create_product( 
    product_in: ProductCreate , 
    product_crud: ProductCRUD = Depends(get_product_crud),
    ):
    return await product_crud.create_product(product_in=product_in)


@router.get("/{product_id}/", response_model=Product)
async def get_product(
    product_id: str,
    product_crud: ProductCRUD = Depends(get_product_crud),
):
    product = await product_crud.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}/")
async def update_product(
    product_id: str, 
    product_update: ProductUpdate, 
    product_crud: ProductCRUD = Depends(get_product_crud),
):
    product = await product_crud.update(product_id, product_update)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/{product_id}")
async def delete_product(
    product_id: str, 
    product_crud: ProductCRUD = Depends(get_product_crud),
):
    """Удаление продукта"""
    success = await product_crud.delete(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}