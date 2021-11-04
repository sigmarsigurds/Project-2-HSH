from fastapi import HTTPException
from APIModels.service_model import ServiceModel
from APIGateway.MerchantGateway import MerchantGateway
from Validations.Validation import Validation


class MerchantExistsValidation(Validation):
    def __init__(self, gateway: MerchantGateway) -> None:
        self.__gateway = gateway
        self.__merchant_id: int = None
        self.__fail_message: str = "Merchant does not exist"

    def validate(self) -> bool:
        valid = self.__gateway.exists(self.__merchant_id)

        if not valid:
            raise HTTPException(status_code=400, detail=self.__fail_message)
        return True

    def set_merchant_id(self, id: int) -> None:
        self.__merchant_id = id

    def get_merchant_id(self) -> int:
        return self.__merchant_id
