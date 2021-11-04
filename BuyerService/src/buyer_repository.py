from buyer_model import BuyerModel
from db_connections.db_connection import DbConnection

"""Save buyer to database"""


class BuyerRepository:
    def __init__(self, connection: DbConnection):
        self.__connection = connection

    def save_buyer(self, name: str, ssn: str, email: str, phone_number: str) -> int:
        buyer = self.__connection.execute(
            f"""
        INSERT INTO buyer(name, ssn, email, phoneNumber) VALUES ('{name}','{ssn}','{email}','{phone_number}') RETURNING id
        """
        )

        self.__connection.commit()

        row = buyer[0]
        return row[0]  # skila id

    def get_buyer(self, id: int) -> str:
        rows = self.__connection.execute(
            f"""
                SELECT * FROM buyer where id = '{id}'
                """
        )
        if len(rows) > 0:
            row = rows[0]
            return BuyerModel(
                buyerId=id,
                name=row[1],
                ssn=row[2],
                email=row[3],
                phoneNumber=row[4],
                # skila nafni
            )
