"""
These validators might be split up more
"""
from fastapi.exceptions import HTTPException
import requests
from APIModels.order_model import OrderModel


def is_request_OK(url: str):
    response = requests.get(url)
    return response.status_code == 200


def is_order_valid(order: OrderModel):
    return validate_merchant_exists(order.merchant_id) and validate_buyer_exists(
        order.buyer_id
    )


def validate_merchant_exists(merchant_id: int) -> bool:
    valid = is_request_OK(f"http://merchant-service-api:8001/merchants/{merchant_id}")

    if not valid:
        raise HTTPException(status_code=400, detail="Merchant does not exist")
    return True


def validate_buyer_exists(buyer_id: int) -> bool:
    valid = is_request_OK(f"http://buyer_container:8002/buyers/{buyer_id}")
    if not valid:
        raise HTTPException(status_code=400, detail="Buyer does not exist")
    return True


def validate_product_exists(product_id: int) -> bool:
    return True


def validate_product_in_stock(product_id: int) -> bool:
    return True


def validate_product_merchant_relation(merchant_id: int, product_id: int) -> bool:
    return True


def validate_merchant_allows_discount(merchant_id: int) -> bool:
    return True
