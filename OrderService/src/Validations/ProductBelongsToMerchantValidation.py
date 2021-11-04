from typing import Optional
from fastapi import HTTPException
import requests
from APIModels.service_model import ServiceModel
from Validations.Validation import Validation


class ProductBelongsToMerchantValidation(Validation):
    def __init__(self, service: ServiceModel) -> None:
        self.__request_url: str = (
            f"http://{service.host}:{service.port}/{service.endpoint}/"
        )
        self.__product_id: int = None
        self.__merchant_id: int = None
        self.__fail_message: str = "Product does not belong to merchant"

    def validate(self) -> bool:

        # Get a response from the InventoryService API
        response = requests.get(f"{self.__request_url}{self.__product_id}")

        # If we didn't get a valid response, that's just akward
        if response.status_code != 200:
            raise HTTPException(
                status_code=418,
                detail="Something went wrong when connecting to the InventoryService API",
            )

        product_merchant_id = response.json().get("merchantId", None)

        # If the merchant id does not match the specified merchant id for the product, throw error
        if not product_merchant_id == self.__merchant_id:
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
