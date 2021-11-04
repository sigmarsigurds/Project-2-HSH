from typing import Optional
import threading
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
import requests

from src.Models import ProductModel, ApiReserveProductModel, ServiceModel
from src.Infrastructure.container import Container
from src.Repositories import (
    InventoryRepository,
    ProductQuantityCanNotBeNegative,
    ProductDoesNotExist,
)

router = APIRouter()


@router.get("/products/{product_id}", status_code=200)
@inject
async def get_product(
    product_id: int,
    merchant_id: Optional[int] = None,
    inventory_repository: InventoryRepository = Depends(
        Provide[Container.inventory_repository_provider]
    ),
):

    """
    This endpoint does not use request body.

    It will try to find a product with the given id, it is also possible to add the merchant id as a
    query parameter to be more precises.

    The responds data if the request is successful:
        {
            "merchantId": int,
            "productName": string,
            "price": Decimal,
            "quantity": int,
            "reserved": int
        }

    If product is not found:
        404 status code

    :param product_id: Id for the product to retrieve
    :param merchant_id: Optional query parameter to get a product with both the product id and merchant id
    :param inventory_repository: Dont modify this
    """
    try:
        product = inventory_repository.get_product(
            product_id=product_id, merchant_id=merchant_id
        )

    except ProductDoesNotExist:
        raise HTTPException(status_code=404, detail="Item not found")

    del product.id  # Remove the product id from the respond data
    return product


@router.post("/products", status_code=201)
@inject
async def save_product(
    product: ProductModel,
    inventory_repository: InventoryRepository = Depends(
        Provide[Container.inventory_repository_provider]
    ),
    merchant_service: ServiceModel = Depends(Provide[Container.merchant_service_model])
):
    """
    This endpoint is used to create product

    Required request body:
        {
            "merchantId": 123,
            "productName": "some  product  name",
            "price": 123.0,
            "quantity": 20
        }

    The responds data if the request is successful:
        {
            "id": int (Product id),
        }

    If product is not found:
        404 status code

    :param product: The request body
    :param inventory_repository: Dont modify this
    """

    # TODO: Get merchant path from docker-compose

    # * Check if merchants exists
    merchant_id = product.merchant_id

    url = merchant_service.get_url(f"/merchants/{merchant_id}")

    respond = requests.get(url)

    if respond.status_code == 404:
        raise HTTPException(status_code=404, detail=f"No merchant with id {merchant_id}")


    new_product = inventory_repository.save_product(product)

    return new_product.id


@router.patch("/products/{product_id}/reserve", status_code=200)
@inject
async def reserves_product(
    product_id: int,
    request_body: ApiReserveProductModel,
    inventory_repository: InventoryRepository = Depends(
        Provide[Container.inventory_repository_provider]
    )
):

    """
    This endpoint receives this request body:
        {
            "quantity": int: (quantity to reserve)
        }

    The responds data if the request is successful:
        {
            "orderId": int,
            buyerEmail: string,
            merchantEmail: string,
            productName: string,
            orderPrice: int,
        }

    If product is not found:
        404 status code

    If the quantity to reserve is more then available quantities:
        403 status code

    :param product_id: Id for product to reserve units
    :param request_body: Has the attribute quantity with number of units to reserve
    :param inventory_repository: Default value
    """
    quantity = request_body.quantity

    try:
        product = inventory_repository.reserve_product(
            product_id=product_id, quantity_to_reserve=quantity
        )

    except ProductDoesNotExist:
        return HTTPException(status_code=404, detail="Product not found")

    except ProductQuantityCanNotBeNegative:
        return HTTPException(status_code=403, detail="Quantity is to high")

    del product.id  # Remove the product id from the respond data
    return product


# ! DELETE THIS
@router.post("/products/{product_id}/sell", status_code=200)
@inject
async def sells_product(
    product_id: int,
    request_body: ApiReserveProductModel,
    inventory_repository: InventoryRepository = Depends(
        Provide[Container.inventory_repository_provider]
    ),
):

    """
    This endpoint receives this request body:
        {
            "quantity": int: (quantity to reserve)
        }

    The responds data if the request is successful:
        {
            "id": int (Product id),
        }

    """

    quantity = request_body.quantity

    product = inventory_repository.sell_product(
        product_id=product_id, quantity_to_free=quantity
    )
    return product


# ! DELETE THIS
@router.post("/products/{product_id}/free_reserved", status_code=200)
@inject
async def free_reserved_product(
    product_id: int,
    request_body: ApiReserveProductModel,
    inventory_repository: InventoryRepository = Depends(
        Provide[Container.inventory_repository_provider]
    ),
):

    """
    This endpoint receives this request body:
        {
            "quantity": int: (quantity to reserve)
        }

    The responds data if the request is successful:
        {
            "id": int (Product id),
        }

    """

    quantity = request_body.quantity

    product = inventory_repository.free_reserved_product(
        product_id=product_id, quantity_to_free=quantity
    )
    return product
