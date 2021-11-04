from typing import Optional
from fastapi import HTTPException
from APIGateway.MerchantGateway import MerchantGateway
from Validations.Validation import Validation


class MerchantAllowsDiscountValidation(Validation):
    def __init__(self, gateway: MerchantGateway) -> None:
        self.__gateway = gateway
        self.__merchant_id: int = None
        self.__fail_message: str = "Merchant does not allow discount"
        self.__order_discount: Optional[float] = None

    def validate(self) -> bool:

        # If the order does not have any discount, we move on the validation, no further checks are needed
        if self.__order_discount is None or self.__order_discount == 0:
            return True

        # If we didn't get a valid response, that's just akward
        if not self.__gateway.exists(self.__merchant_id):
            raise HTTPException(
                status_code=418,
                detail="Merchant does not exist",
            )

        # If the order has a discount on it and the merchant does not allow discounts, send error
        if not self.__gateway.allows_discount(self.__merchant_id):
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
