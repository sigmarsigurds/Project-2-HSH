import requests
from APIModels.service_model import ServiceModel
from APIModels.buyer_model import BuyerModel


class BuyerGateway:
    def __init__(self, service: ServiceModel) -> None:
        self.__service = service
        self.__url = f"http://{service.host}:{service.port}/{service.endpoint}/"

    def get_buyer_email(self, buyer_id: int) -> str:
        buyer = self.__get_buyer(buyer_id)
        return buyer.buyer_id

    def exists(self, buyer_id: int) -> bool:
        buyer = self.__get_buyer(buyer_id)
        if buyer:
            return True
        return False

    def get_host(self) -> str:
        return self.__service.host

    def get_port(self) -> str:
        return self.__service.port

    def get_endpoint(self) -> str:
        return self.__service.endpoint

    def __get_buyer(self, buyer_id: int) -> BuyerModel:
        url = f"{self.__url}{buyer_id}"
        response = requests.get(url)

        if response.status_code != 200:
            return None

        return self.__assemble_buyer(buyer_data=response.json(), buyer_id=buyer_id)

    def __assemble_buyer(self, buyer_data: dict, buyer_id: int) -> BuyerModel:
        return BuyerModel(
            buyerId=buyer_id,
            name=buyer_data.get("name", None),
            ssn=buyer_data.get("ssn", None),
            email=buyer_data.get("email", -1),
            phoneNumber=buyer_data.get("phoneNumber", -1),
        )
