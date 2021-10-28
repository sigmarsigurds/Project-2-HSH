from typing import List

from Validations.Validation import Validation


class OrderValidator(Validation):
    __validations: List[Validation] = []

    def validate(self) -> bool:
        for validation in self.__validations:
            validation.validate()
        return True

    def add_validation(self, validation: Validation) -> None:
        self.__validations.append(validation)

    def clear_validations(self):
        self.__validations: List[Validation] = []
