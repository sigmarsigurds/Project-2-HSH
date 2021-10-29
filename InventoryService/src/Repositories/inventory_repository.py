from typing import Optional, Tuple

from src.DbConnections import DbConnection
from src.Models import ProductModel


class InventoryRepository:
    def __init__(self, db_connection: DbConnection = None):
        self.__db_connection = db_connection

    @staticmethod
    def __create_product_from_tuple(data: Tuple) -> ProductModel:
        product_id, merchant_id, product_name, price, quantity, reserved = data

        return ProductModel(
            id=product_id,
            merchant_id=merchant_id,
            product_name=product_name,
            price=price,
            quantity=quantity,
            reserved=reserved
        )

    def save_product(self, product: ProductModel) -> ProductModel:
        values = f"(DEFAULT, '{product.merchant_id}', '{product.name}', '{product.price}', '{product.quantity}', " \
                 f"DEFAULT) "

        query = f"INSERT INTO Product VALUES {values} RETURNING *"

        data = self.__db_connection.execute(query)

        self.__db_connection.commit()

        if len(data) > 0:
            new_product = self.__create_product_from_tuple(data[0])

            return new_product


    def get_product(self, product_id: int) -> Optional[ProductModel]:
        query = f"SELECT * from Product where id = '{product_id}'"

        data = self.__db_connection.execute(query)

        if len(data) > 0:
            product = self.__create_product_from_tuple(data[0])

            return product
