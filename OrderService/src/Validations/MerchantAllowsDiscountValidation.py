from typing import Optional
from fastapi import HTTPException
import requests
from APIModels.service_model import ServiceModel
from Validations.Validation import Validation


class MerchantAllowsDiscountValidation(Validation):
    def __init__(self, service: ServiceModel) -> None:
        self.__request_url: str = (
            f"http://{service.host}:{service.port}/{service.endpoint}/"
        )
        self.__merchant_id: int = None
        self.__fail_message: str = "Merchant does not allow discount"
        self.__order_discount: Optional[float] = None

    def validate(self) -> bool:

        # If the order does not have any discount, we move on the validation, no further checks are needed
        if self.__order_discount is None or self.__order_discount == 0:
            return True

        # Get a response from the MerchantService API
        response = requests.get(f"{self.__request_url}{self.__merchant_id}")

        # If we didn't get a valid response, that's just akward
        if response.status_code != 200:
            raise HTTPException(
                status_code=418,
                detail="Something went wrong when connecting to the MerchantService API",
            )

        allows_discount = response.json().get("allowsDiscount", False)

        # If the order has a discount on it and the merchant does not allow discounts, send error
        if not allows_discount:
            raise HTTPException(status_code=400, detail=self.__fail_message)

        # If the order has a discount on it and the merchant does allow discounts, check if the number is range ]0,1]
        if not (0 < self.__order_discount <= 1):
            raise HTTPException(status_code=400, detail="Discount is invalid")

        # If all checks are valid, validate the discount
        return True

    def set_merchant_id(self, id: int) -> None:
        self.__merchant_id = id

    def get_merchant_id(self) -> int:
        return self.__merchant_id

    def set_order_discount(self, discount: float) -> None:
        self.__order_discount = discount

    def get_order_discount(self) -> Optional[float]:
        return self.__order_discount
