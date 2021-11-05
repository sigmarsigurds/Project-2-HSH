from typing import List

from src.Models import OrderPaymentInformationModel, TransactionModel
from src.Validators import CreditCardValidator, InvalidCreditCard
from src.Repositories import TransactionRepository


class Transaction:
    def __init__(self, credit_card_validator: CreditCardValidator, transaction_repository: TransactionRepository):
        self.credit_card_validator = credit_card_validator
        self.transaction_repository = transaction_repository

    def preform_transaction(self, order_payment_information: OrderPaymentInformationModel):

        transaction = TransactionModel(order_id=order_payment_information.order_id)

        try:
            self.credit_card_validator.validate(order_payment_information.credit_card)

        except InvalidCreditCard:
            self.transaction_repository.save_transaction(transaction)

            raise InvalidCreditCard

        # * Do transaction
        # * / Do transaction

        # * Transaction successful
        transaction.success = True

        self.transaction_repository.save_transaction(transaction)
