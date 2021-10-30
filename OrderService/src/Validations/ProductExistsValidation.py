from fastapi import HTTPException
from APIModels.service_model import ServiceModel
from Validations.Validation import Validation


class ProductExistsValidation(Validation):
    def __init__(self, service: ServiceModel) -> None:
        self.__request_url: str = (
            f"http://{service.host}:{service.port}/{service.endpoint}/"
        )
        self.__product_id: int = None
        self.__fail_message: str = "Product does not exist"

    def validate(self) -> bool:
        valid = self.request_ok(url=f"{self.__request_url}{self.__product_id}")

        if not valid:
            raise HTTPException(status_code=400, detail=self.__fail_message)
        return True

    def set_product_id(self, id: int) -> None:
        self.__product_id = id

    def get_product_id(self) -> int:
        return self.__product_id
