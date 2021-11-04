import requests
from APIModels.service_model import ServiceModel
from APIModels.merchant_model import MerchantModel


class MerchantGateway:
    def __init__(self, service: ServiceModel) -> None:
        self.__service = service
        self.__url = f"http://{service.host}:{service.port}/{service.endpoint}/"

    def allows_discount(self, merchant_id: int) -> bool:
        merchant = self.__get_merchant(merchant_id)
        return merchant.allows_discount

    def get_merchant_email(self, merchant_id: int) -> str:
        merchant = self.__get_merchant(merchant_id)
        return merchant.email

    def exists(self, merchant_id: int) -> bool:
        merchant = self.__get_merchant(merchant_id)
        if merchant:
            return True
        return False

    def get_host(self) -> str:
        return self.__service.host

    def get_port(self) -> str:
        return self.__service.port

    def get_endpoint(self) -> str:
        return self.__service.endpoint

    def __get_merchant(self, merchant_id: int) -> MerchantModel:
        url = f"{self.__url}{merchant_id}"
        response = requests.get(url)

        if response.status_code != 200:
            return None

        return self.__assemble_merchant(
            merchant_data=response.json(), merchant_id=merchant_id
        )

    def __assemble_merchant(
        self, merchant_data: dict, merchant_id: int
    ) -> MerchantModel:
        return MerchantModel(
            merchantId=merchant_id,
            name=merchant_data.get("name", None),
            ssn=merchant_data.get("ssn", None),
            email=merchant_data.get("email", None),
            phoneNumber=merchant_data.get("phoneNumber", None),
            allowsDiscount=merchant_data.get("allowsDiscount", False),
        )
