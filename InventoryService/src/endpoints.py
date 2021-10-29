from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from src.Models.product_model import ProductModel
from src.Infrastructure.container import Container
from src.Repositories import InventoryRepository

router = APIRouter()


@router.get('/products/{product_id}', status_code=200)
@inject
async def get_product(
        product_id: int,
        inventory_repository: InventoryRepository = Depends(
            Provide[Container.inventory_repository_provider])):

    product = inventory_repository.get_product(product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"data": product}


@router.post('/products', status_code=201)
@inject
async def save_product(
        product: ProductModel,
        inventory_repository: InventoryRepository = Depends(
            Provide[Container.inventory_repository_provider])):

    new_product = inventory_repository.save_product(product)

    return {"data": new_product}
