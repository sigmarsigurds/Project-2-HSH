from fastapi import HTTPException
from APIModels.service_model import ServiceModel
from Validations.Validation import Validation


class BuyerExistsValidation(Validation):
    def __init__(self, service: ServiceModel) -> None:
        self.__request_url: str = (
            f"http://{service.host}:{service.port}/{service.endpoint}/"
        )
        self.__buyer_id: int = None
        self.__fail_message: str = "Buyer does not exist"

    def validate(self) -> bool:
        valid = self.request_ok(url=f"{self.__request_url}{self.__buyer_id}")

        if not valid:
            raise HTTPException(status_code=400, detail=self.__fail_message)
        return True

    def set_buyer_id(self, id: int) -> None:
        self.__buyer_id = id

    def get_buyer_id(self) -> int:
        return self.__buyer_id
