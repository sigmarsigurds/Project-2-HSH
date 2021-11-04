import requests
from APIModels.service_model import ServiceModel
from APIModels.product_model import ProductModel


class InventoryGateway:
    def __init__(self, service: ServiceModel) -> None:
        self.__service = service
        self.__url = f"http://{service.host}:{service.port}/{service.endpoint}/"

    def reserve(self, product_id: int, amount: int = 1) -> ProductModel:
        url = f"{self.__url}{product_id}/reserve"
        response = requests.patch(url=url, json={"quantity": amount})

        if response.status_code != 200:
            return None

        return self.__assemble_product(
            product_data=response.json(), product_id=product_id
        )

    def get_quantity_amount(self, product_id: int) -> int:
        product = self.__get_product(product_id)
        return product.quantity

    def get_reserved_amount(self, product_id: int) -> int:
        product = self.__get_product(product_id)
        return product.reserved

    def get_available_quantity(self, product_id: int) -> int:
        product = self.__get_product(product_id)
        return product.quantity - product.reserved

    def get_merchant_id(self, product_id: int) -> int:
        product = self.__get_product(product_id)
        return product.merchant_id

    def exists(self, product_id: int) -> bool:
        product = self.__get_product(product_id)
        if product:
            return True
        return False

    def get_host(self) -> str:
        return self.__service.host

    def get_port(self) -> str:
        return self.__service.port

    def get_endpoint(self) -> str:
        return self.__service.endpoint

    def __get_product(self, product_id: int) -> ProductModel:
        url = f"{self.__url}{product_id}"
        response = requests.get(url)

        if response.status_code != 200:
            return None

        return self.__assemble_product(
            product_data=response.json(), product_id=product_id
        )

    def __assemble_product(self, product_data: dict, product_id: int) -> ProductModel:
        return ProductModel(
            productId=product_id,
            merchantId=product_data.get("merchantId", -1),
            productName=product_data.get("productName", None),
            price=product_data.get("price", -1),
            quantity=product_data.get("quantity", -1),
            reserved=product_data.get("reserved", -1),
        )
