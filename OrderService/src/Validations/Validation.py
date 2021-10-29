from abc import ABC, abstractmethod
import requests


class Validation(ABC):
    def request_ok(self, url):
        response = requests.get(url)
        return response.status_code == 200

    @abstractmethod
    def validate(self) -> bool:
        ...
