from buyer_model import BuyerModel
from db_connections.db_connection import DbConnection

"""Save buyer to database"""


class BuyerRepository:
    def __init__(self, connection: DbConnection):
        self.__connection = connection

    def save_buyer(self, name: str, ssn: str, email: str, phonenumber: str) -> int:
        buyer = self.__connection.execute(
            f"""
        INSERT INTO buyer(name, ssn, email, phonenumber) VALUES ('{name}','{ssn}','{email}','{phonenumber}') RETURNING id
        """
        )

        self.__connection.commit()

        row = buyer[0]
        return row[0]  # skila id

    def get_buyer(self, id: int) -> str:
        buyer = self.__connection.execute(
            f"""
                SELECT * FROM buyer where id = '{id}'
                """
        )

        row = buyer[0]
        return row[1], row[2], row[3], row[4]  # skila nafni
