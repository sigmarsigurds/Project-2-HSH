from abc import ABC, abstractmethod


class Validation(ABC):
    @abstractmethod
    def validate(self) -> bool:
        ...
