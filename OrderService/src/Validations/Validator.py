from typing import List

from Validations.Validation import Validation


class Validator(Validation):
    __validations: List[Validation] = []

    def validate(self) -> bool:
        for validation in self.__validations:
            if not validation.validate():
                return False
        return True

    def add_validation(self, validation: Validation) -> None:
        self.__validations.append(validation)
