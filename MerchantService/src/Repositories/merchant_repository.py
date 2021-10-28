from typing import Optional, Tuple

from src.DbConnections import DbConnection
from src.Models import MerchantModel


class MerchantRepository:
    def __init__(self, db_connection: DbConnection = None):
        self.__db_connection = db_connection

    @staticmethod
    def __create_merchant_from_tuple(data: Tuple) -> MerchantModel:
        merchant_id, name, ssn, email, phone_number, allows_discount = data

        return MerchantModel(
            id=merchant_id,
            name=name,
            ssn=ssn,
            email=email,
            phoneNumber=phone_number,
            allowsDiscount=allows_discount
        )

    def save_merchant(self, merchant: MerchantModel) -> MerchantModel:
        values = f"(DEFAULT, '{merchant.name}', '{merchant.ssn}', '{merchant.email}', '{merchant.phone_number}', '{merchant.allows_discount}')"

        query = f"INSERT INTO Merchant VALUES {values} RETURNING *"

        data = self.__db_connection.execute(query)

        self.__db_connection.commit()

        if len(data) > 0:
            merchant = self.__create_merchant_from_tuple(data[0])

            return merchant


    def get_merchant(self, merchant_id: int) -> Optional[MerchantModel]:
        query = f"SELECT * from Merchant where id = '{merchant_id}'"

        data = self.__db_connection.execute(query)

        if len(data) > 0:
            merchant = self.__create_merchant_from_tuple(data[0])

            return merchant
