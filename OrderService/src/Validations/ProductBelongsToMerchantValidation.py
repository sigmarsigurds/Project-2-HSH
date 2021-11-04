from typing import Optional
from fastapi import HTTPException
import requests
from APIModels.service_model import ServiceModel
from APIGateway.InventoryGateway import InventoryGateway
from Validations.Validation import Validation


class ProductBelongsToMerchantValidation(Validation):
    def __init__(self, gateway: InventoryGateway) -> None:
        self.__gateway = gateway
        self.__product_id: int = None
        self.__merchant_id: int = None
        self.__fail_message: str = "Product does not belong to merchant"

    def validate(self) -> bool:

        # If we didn't get a valid response, that's just akward
        if not self.__gateway.exists(self.__product_id):
            raise HTTPException(
                status_code=404,
                detail="Product does not exist",
            )

        # If the merchant id does not match the specified merchant id for the product, throw error
        if not self.__gateway.get_merchant_id(self.__product_id) == self.__merchant_id:
            raise HTTPException(status_code=400, detail=self.__fail_message)

        # If all checks are valid, validate the discount
        return True

    def set_product_id(self, id: int) -> None:
        self.__product_id = id

    def get_product_id(self) -> int:
        return self.__product_id

    def set_merchant_id(self, id: int) -> None:
        self.__merchant_id = id

    def get_merchant_id(self) -> int:
        return self.__merchant_id
