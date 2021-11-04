from typing import Optional, Tuple

from src.DbConnections import DbConnection
from src.Models import OrderPaymentInformationModel, CreditCardModel, TransactionModel


class TransactionDoesNotExist(Exception):
    """
    Transaction dose not exist
    """


class TransactionRepository:
    def __init__(self, db_connection: DbConnection = None):
        self.__db_connection = db_connection

    @staticmethod
    def __create_transaction_model_from_tuple(data: Tuple) -> TransactionModel:
        transaction_id, order_id, success = data

        return TransactionModel(
            id=transaction_id,
            order_id=order_id,
            success=success
        )


    def save_transaction(self, transaction: TransactionModel) -> TransactionModel:
        values = f"(DEFAULT, '{transaction.order_id}', '{transaction.success}'"

        query = f"INSERT INTO Payment_Transaction VALUES {values} RETURNING *"

        data = self.__db_connection.execute(query)

        self.__db_connection.commit()

        if len(data) > 0:
            new_product = self.__create_transaction_model_from_tuple(data[0])

            return new_product


    def get_transaction(self, transaction_id: int) -> Optional[TransactionModel]:
        query = f"SELECT * from Payment_Transaction where id = '{transaction_id}'"

        data = self.__db_connection.execute(query)

        if len(data) > 0:
            product = self.__create_transaction_model_from_tuple(data[0])

            return product

        else:
            raise TransactionDoesNotExist()






