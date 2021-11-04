from src.Models.credit_card_model import CreditCardModel


class InvalidCreditCard(Exception):
    pass


class CreditCardValidator:
    START_MONTH = 1
    END_MONTH = 12
    YEAR_LENGTH = 4
    CVC_LENGTH = 3

    def __validate_card(self, card_number: str):
        def luhn_checksum(card_number):
            def digits_of(n):
                return [int(d) for d in str(n)]

            digits = digits_of(card_number)
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = 0
            checksum += sum(odd_digits)
            for d in even_digits:
                checksum += sum(digits_of(d * 2))
            return checksum % 10

        if not luhn_checksum(card_number) == 0:
            print("Card validation failed")
            raise InvalidCreditCard()
        print("Card validation succeeded")

        # print('Valid') if luhn_checksum("4532015112830366")==0 else print('Invalid')

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
        self.__validate_card(credit_card.card_number)
        self.__validate_month(credit_card.expiration_month)
        self.__validate_year(credit_card.expiration_year)
        self.__validate_cvc(credit_card.cvc)
