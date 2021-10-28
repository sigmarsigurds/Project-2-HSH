from abc import ABC, abstractmethod
import requests


class Validation(ABC):
    def request_ok(self, url):
        response = requests.get(url)
        print("Fetching from")
        print(url)
        print(f"Status code: {response.status_code}")
        return response.status_code == 200

    @abstractmethod
    def validate(self) -> bool:
        ...
