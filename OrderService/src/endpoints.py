from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
import requests

from APIModels.order_request_model import OrderRequestModel
from APIModels.order_response_model import OrderResponseModel
from Infrastructure.container import Container
from APIModels.order_database_model import OrderDatabaseModel
from APIModels.order_email_information_model import OrderEmailInformationModel
from APIModels.order_payment_information_model import OrderPaymentInformationModel
from APIModels.credit_card_model import CreditCardModel
from APIModels.service_model import ServiceModel
from APIModels.product_model import ProductModel
from APIGateway.BuyerGateway import BuyerGateway
from APIGateway.InventoryGateway import InventoryGateway
from APIGateway.MerchantGateway import MerchantGateway
from Validations.ProductBelongsToMerchantValidation import (
    ProductBelongsToMerchantValidation,
)
from Validations.ProductInStockValidation import ProductInStockValidation
from Validations.ProductExistsValidation import ProductExistsValidation
from Tools.FormatCreditCardNumber import FormatCreditCardNumber
from Validations.MerchantAllowsDiscountValidation import (
    MerchantAllowsDiscountValidation,
)
from Validations.BuyerExistsValidation import BuyerExistsValidation
from Validations.MerchantExistsValidation import MerchantExistsValidation
from Validations.OrderValidator import OrderValidator
from Repositories.order_repository import OrderRepository
from order_sender import OrderSender

router = APIRouter()


@router.get("/orders/{id}", status_code=200)
@inject
async def get_order(
    id: int,
    order_repository: OrderRepository = Depends(
        Provide[Container.order_repository_provider]
    ),
):

    order: OrderDatabaseModel = order_repository.get_order(id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order does not exist")
    return OrderResponseModel(
        productId=order.product_id,
        merchantId=order.merchant_id,
        buyerId=order.buyer_id,
        cardNumber=order.card_number,
        totalPrice=order.total_price,
    )


@router.post("/orders", status_code=201)
@inject
async def save_order(
    order_request: OrderRequestModel,
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
    product_exists_validation: ProductExistsValidation = Depends(
        Provide[Container.product_exists_validation_provider]
    ),
    product_in_stock_validation: ProductInStockValidation = Depends(
        Provide[Container.product_in_stock_validation_provider]
    ),
    product_belongs_to_merchant_validation: ProductBelongsToMerchantValidation = Depends(
        Provide[Container.product_belongs_to_merchant_validation_provider]
    ),
    inventory_gateway: InventoryGateway = Depends(
        Provide[Container.inventory_gateway_provider]
    ),
    merchant_gateway: MerchantGateway = Depends(
        Provide[Container.merchant_gateway_provider]
    ),
    buyer_gateway: BuyerGateway = Depends(Provide[Container.buyer_gateway_provider]),
):

    # Empty any previous validations
    order_validator.clear_validations()

    # Check if merchant exists
    merchant_exists_validation.set_merchant_id(order_request.merchant_id)

    # Check if buyer exists
    buyer_exists_validation.set_buyer_id(order_request.buyer_id)

    # Check if discount is valid and allowed
    merchant_allows_discount_validation.set_merchant_id(order_request.merchant_id)
    merchant_allows_discount_validation.set_order_discount(order_request.discount)

    # Check if product exists
    product_exists_validation.set_product_id(order_request.product_id)

    # Check if product is in stock
    product_in_stock_validation.set_product_id(order_request.product_id)

    # Check if product belongs to merchant
    product_belongs_to_merchant_validation.set_product_id(order_request.product_id)
    product_belongs_to_merchant_validation.set_merchant_id(order_request.merchant_id)

    order_validator.add_validations(
        [
            merchant_exists_validation,
            buyer_exists_validation,
            merchant_allows_discount_validation,
            product_exists_validation,
            product_in_stock_validation,
            product_belongs_to_merchant_validation,
        ]
    )

    # Execute all checks above and raise errors if anything is invalid
    order_validator.validate()

    """
    * Done
    Then OrderService communicates next with the InventoryService with request/response based communication 
    and reserves a product with product_id. 
    """

    product = inventory_gateway.reserve(order_request.product_id)

    if product is None:
        raise HTTPException(
            status_code=400,
            detail="Inventory Service was not able to reserve the product",
        )

    """
    If OrderServicec was successful in reserving the product (the product wasn’t sold out / the product exists) 
    then OrderServices stores the order in it’s database and sends out an event that the order has been created.
    """
    order_database: OrderDatabaseModel = order_repository.save_order(
        order_request, product
    )

    merchant_email = merchant_gateway.get_merchant_email(order_request.merchant_id)
    buyer_email = buyer_gateway.get_buyer_email(order_request.buyer_id)

    order_email_information = OrderEmailInformationModel(
        orderId=order_database.order_id,
        buyerEmail=buyer_email,
        merchantEmail=merchant_email,
        productName=product.product_name,
        orderPrice=order_database.total_price,
    )

    order_payment_information = OrderPaymentInformationModel(
        orderId=order_database.order_id,
        buyerEmail=buyer_email,
        merchantEmail=merchant_email,
        productId=order_database.product_id,
        merchantId=order_database.merchant_id,
        creditCard=order_request.credit_card,
    )

    order_sender.send_order_email(order_email_information)
    order_sender.send_order_payment(order_payment_information)

    return order_database.order_id
