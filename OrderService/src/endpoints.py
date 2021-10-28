from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from APIModels.order_request_model import OrderRequestModel
from APIModels.order_response_model import OrderResponseModel
from Infrastructure.container import Container
from APIModels.order_database_model import OrderDatabaseModel
from Validations.MerchantAllowsDiscountValidation import (
    MerchantAllowsDiscountValidation,
)
from Validations.BuyerExistsValidation import BuyerExistsValidation
from Validations.MerchantExistsValidation import MerchantExistsValidation
from Validations.OrderValidator import OrderValidator
from Repositories.order_repository import OrderRepository
from order_sender import OrderSender
from Validations.is_order_valid import is_order_valid

router = APIRouter()


@router.get("/orders/{id}", status_code=200)
@inject
async def get_order(
    id: int,
    order_repository: OrderRepository = Depends(
        Provide[Container.order_repository_provider]
    ),
):
    # TODO: get order with id
    # TODO: Again, ask the typing pervert how to do OrderModel OR None
    order: OrderDatabaseModel = order_repository.get_order(id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order does not exist")
    print("supsup")
    return {
        "data": OrderResponseModel(
            orderId=order.order_id,
            productId=order.product_id,
            merchantId=order.merchant_id,
            buyerId=order.buyer_id,
            cardNumber=order.credit_card.card_number,
            totalPrice=order.discount,
        )
    }


@router.post("/orders", status_code=201)
@inject
async def save_order(
    order: OrderRequestModel,
    order_sender: OrderSender = Depends(Provide[Container.order_sender_provider]),
    order_repository: OrderRepository = Depends(
        Provide[Container.order_repository_provider]
    ),
    order_validator: OrderValidator = Depends(
        Provide[Container.order_validator_provider]
    ),
    merchant_exists_validation: MerchantExistsValidation = Depends(
        Provide[Container.merchant_exists_validation_provider]
    ),
    merchant_allows_discount_validation: MerchantAllowsDiscountValidation = Depends(
        Provide[Container.merchant_allows_discount_validation_provider]
    ),
    buyer_exists_validation: BuyerExistsValidation = Depends(
        Provide[Container.buyer_exists_validation_provider]
    ),
):
    """
    * DONE
    • OrderService should return 400 HTTP Status Code with the error message "Merchant does not exist" if there is no merchant with the specific merchantId.
    • OrderService should return 400 HTTP Status Code with the error message "Buyer does not exist" if there is not buyer with the specific buyerId
    • OrderService should return 400 HTTP Status Code with the error message "Merchant does not allow discount" if merchant with merchantId does not allow discounts and the specified discount is something other then null or 0.
    * NOT READY
    • OrderService should return 400 HTTP Status Code with the error message "Product does not exist" if there is no product with the specific productId
    • OrderService should return 400 HTTP Status Code with the error message "Product is sold out" if a product with the specific productId is sold out.
    • OrderService should return 400 HTTP Status Code with the error message "Product does not belong to merchant" if product with productId does not belong to merchant with merchantId.
    • If all the validations are successful then the OrderSErvie should reserve the product, store it in the database, send an event that the order has been created and return 201 HTTP Status Code með order id-i sem response message.
    """

    # Empty any previous validations
    order_validator.clear_validations()

    # Check if merchant exists
    merchant_exists_validation.set_merchant_id(order.merchant_id)
    order_validator.add_validation(merchant_exists_validation)

    # Check if buyer exists
    buyer_exists_validation.set_buyer_id(order.buyer_id)
    order_validator.add_validation(buyer_exists_validation)

    # Check if discount is valid and allowed
    merchant_allows_discount_validation.set_merchant_id(order.merchant_id)
    merchant_allows_discount_validation.set_order_discount(order.discount)
    order_validator.add_validation(merchant_allows_discount_validation)

    # TODO: Look into background_tasks for something like this (https://youtu.be/ESVwKQLldjg?t=1065)
    # Execute all checks above and raise errors if anything is invalid
    valid = order_validator.validate()

    if valid:

        order: OrderDatabaseModel = order_repository.save_order(order)

        return {
            "data": OrderResponseModel(
                orderId=order.order_id,
                productId=order.product_id,
                merchantId=order.merchant_id,
                buyerId=order.buyer_id,
                cardNumber=order.credit_card.card_number,
                totalPrice=-1,
            )
        }
