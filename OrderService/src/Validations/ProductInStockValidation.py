from fastapi import HTTPException
import requests
from APIModels.service_model import ServiceModel
from Validations.Validation import Validation


class ProductInStockValidation(Validation):
    def __init__(self, service: ServiceModel) -> None:
        self.__request_url: str = (
            f"http://{service.host}:{service.port}/{service.endpoint}/"
        )
        self.__product_id: int = None
        self.__fail_message: str = "Product is sold out"

    def validate(self) -> bool:
        data: dict = requests.get(url=f"{self.__request_url}{self.__product_id}").json()

        # * Maybe this logic should be done by inventory
        quantity = data.get("quantity", 0)
        reserved = data.get("reserved", 0)

        valid = (quantity - reserved) > 0

        if not valid:
            raise HTTPException(status_code=400, detail=self.__fail_message)
        return True

    def set_product_id(self, id: int) -> None:
        self.__product_id = id

    def get_product_id(self) -> int:
        return self.__product_id
