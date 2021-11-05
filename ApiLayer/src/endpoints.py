from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Response
import requests
import json

from src.ApiModels import OrderRequestModel, MerchantModel, ProductModel, BuyerModel, ServiceModel
from src.Infrastructure.container import Container

router = APIRouter()


@router.get("/orders/{order_id}")
@inject
async def get_order(order_id: int, response: Response,
                    order_service_endpoint: ServiceModel = Depends(
                        Provide[Container.order_service_endpoint_provider]
                    )
                    ):

    proxy = requests.get(order_service_endpoint.get_url(f"/orders/{order_id}"))

    response.status_code = proxy.status_code
    return json.loads(proxy.content)


@router.post("/orders")
@inject
async def create_order(
        order_request: OrderRequestModel, response: Response,
        order_service_endpoint: ServiceModel = Depends(
            Provide[Container.order_service_endpoint_provider]
        )
):
    proxy = requests.post(order_service_endpoint.get_url("/orders"), data=order_request.json())

    response.status_code = proxy.status_code
    return json.loads(proxy.content)


@router.get("/merchants/{merchant_id}")
@inject
async def get_merchants(merchant_id: int, response: Response,
                        merchant_service_endpoint: ServiceModel = Depends(
                            Provide[Container.merchant_service_endpoint_provider]
                        )
                        ):
    proxy = requests.get(merchant_service_endpoint.get_url(f"/merchants/{merchant_id}"))

    response.status_code = proxy.status_code
    return json.loads(proxy.content)


@router.post("/merchants")
@inject
async def create_merchants(
        merchant: MerchantModel, response: Response,
        merchant_service_endpoint: ServiceModel = Depends(
            Provide[Container.merchant_service_endpoint_provider]
        )
):
    proxy = requests.post(merchant_service_endpoint.get_url(f"/merchants"), data=merchant.json())

    response.status_code = proxy.status_code
    return json.loads(proxy.content)


@router.get("/buyers/{buyer_id}")
@inject
async def get_buyers(buyer_id: int, response: Response,

                     buyer_service_endpoint: ServiceModel = Depends(
                         Provide[Container.buyer_service_endpoint_provider]
                     )
                     ):
    proxy = requests.get(buyer_service_endpoint.get_url(f"/buyers/{buyer_id}"))

    response.status_code = proxy.status_code
    return json.loads(proxy.content)


@router.post("/buyers")
@inject
async def create_buyers(buyer: BuyerModel, response: Response,

                        buyer_service_endpoint: ServiceModel = Depends(
                            Provide[Container.buyer_service_endpoint_provider]
                        )
                        ):
    proxy = requests.post(buyer_service_endpoint.get_url(f"/buyers"), data=buyer.json())

    response.status_code = proxy.status_code
    return json.loads(proxy.content)


@router.get("/products/{products_id}")
@inject
async def get_products(products_id: int, response: Response,
                       inventory_service_endpoint: ServiceModel = Depends(
                           Provide[Container.inventory_service_endpoint_provider]
                       )
                       ):
    proxy = requests.get(inventory_service_endpoint.get_url(f"/products/{products_id}"))

    response.status_code = proxy.status_code
    return json.loads(proxy.content)


@router.post("/products")
@inject
async def create_products(product: ProductModel, response: Response,
                          inventory_service_endpoint: ServiceModel = Depends(
                              Provide[Container.inventory_service_endpoint_provider]
                          )
                          ):
    proxy = requests.post(inventory_service_endpoint.get_url(f"/products"), product.json())

    response.status_code = proxy.status_code
    return json.loads(proxy.content)
