from typing import Optional, Tuple

from src.DbConnections import DbConnection
from src.Models import ProductModel


class ProductDoesNotExist(Exception):
    """
    This error happens when a product is not found with the given id or other identifiers.
    """


class ProductQuantityCanNotBeNegative(Exception):
    """
    The current operation would make the quantity for specific product negative. That is not allowed.
    """


class InventoryRepository:
    def __init__(self, db_connection: DbConnection = None):
        self.__db_connection = db_connection

    @staticmethod
    def __create_product_from_tuple(data: Tuple) -> ProductModel:
        product_id, merchant_id, product_name, price, quantity, reserved = data

        return ProductModel(
            id=product_id,
            merchantId=merchant_id,  # This needs to be camel case, beaches this model is also use for receiving
            productName=product_name,  # request from clients, and whe are using alias to allow the JSON to be camel
            price=price,  # case
            quantity=quantity,
            reserved=reserved,
        )

    def save_product(self, product: ProductModel) -> ProductModel:
        values = (
            f"(DEFAULT, '{product.merchant_id}', '{product.name}', '{product.price}', '{product.quantity}', "
            f"DEFAULT) "
        )

        query = f"INSERT INTO Product VALUES {values} RETURNING *"

        data = self.__db_connection.execute(query)

        self.__db_connection.commit()

        if len(data) > 0:
            new_product = self.__create_product_from_tuple(data[0])

            return new_product

    def get_product(
        self, product_id: int, merchant_id: int = None
    ) -> Optional[ProductModel]:
        query = f"SELECT * from Product where id = '{product_id}'"

        if merchant_id is not None:
            query += f" AND merchant_id = '{merchant_id}'"

        data = self.__db_connection.execute(query)

        if len(data) > 0:
            product = self.__create_product_from_tuple(data[0])

            return product

        else:
            raise ProductDoesNotExist()

    def reserve_product(
        self, product_id: int, quantity_to_reserve: int
    ) -> Optional[ProductModel]:
        """

        :param product_id: The id for a product to update
        :param quantity_to_reserve: How many units to reserve
        :return: Updated product
        """

        # ? Checking if it is allowed to reserved quantities should maybe be in separate function

        product = self.get_product(product_id=product_id)

        current_reserved_quantity = product.reserved

        if product.quantity - (current_reserved_quantity + quantity_to_reserve) < 0:
            raise ProductQuantityCanNotBeNegative()

        current_reserved_quantity += quantity_to_reserve

        query = f"UPDATE Product SET reserved = {current_reserved_quantity} WHERE id = {product_id} RETURNING *"

        data = self.__db_connection.execute(query)

        self.__db_connection.commit()

        if len(data) > 0:
            product = self.__create_product_from_tuple(data[0])

            return product

    def free_reserved_product(self, product_id: int, quantity_to_free: int):
        # TODO: free reserved product
        # product quantity- quantity to free
        # product reserved quantity - quantity to free
        product = self.get_product(product_id=product_id)
        current_reserved_quantity = product.reserved
        current_reserved_quantity -= quantity_to_free

        current_product_quantity = product.quantity
        current_product_quantity -= quantity_to_free

        query_reserved = f"UPDATE Product SET reserved = {current_reserved_quantity} WHERE id = {product_id} RETURNING *"
        query_product = f"UPDATE Product SET quantity = {current_product_quantity} WHERE id = {product_id} RETURNING *"

        data = self.__db_connection.execute(query_reserved)
        data = self.__db_connection.execute(query_product)

        self.__db_connection.commit()
        product = self.get_product(product_id=product_id)
        if len(data) > 0:
            product = self.__create_product_from_tuple(data[0])

            return product

    def sell_product(self, product_id: int, quantity_to_free):
        # product quantity- quantity to free

        product = self.get_product(product_id=product_id)
        current_product_quantity = product.quantity
        current_product_quantity -= quantity_to_free

        query = f"UPDATE Product SET quantity = {current_product_quantity} WHERE id = {product_id} RETURNING *"
        data = self.__db_connection.execute(query)

        self.__db_connection.commit()
        product = self.get_product(product_id=product_id)
        if len(data) > 0:
            product = self.__create_product_from_tuple(data[0])

            return product
