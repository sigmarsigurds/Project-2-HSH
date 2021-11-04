from src.Models.credit_card_model import CreditCardModel


class InvalidCreditCard(Exception):
    pass


class CreditCardValidator:
    START_MONTH = 1
    END_MONTH = 12
    YEAR_LENGTH = 4
    CVC_LENGTH = 3

    def __validate_month(self, month: int):
        if not (self.START_MONTH <= month <= self.END_MONTH):
            raise InvalidCreditCard()


    def __validate_year(self, year: int):
        if len(str(year)) != self.YEAR_LENGTH:
            raise InvalidCreditCard()


    def __validate_cvc(self, cvc: str):
        if len(cvc) != self.CVC_LENGTH:
            raise InvalidCreditCard()

    def validate(self, credit_card: CreditCardModel):
        self.__validate_month(credit_card.expiration_month)
        self.__validate_year(credit_card.expiration_year)
        self.__validate_cvc(credit_card.cvc)
