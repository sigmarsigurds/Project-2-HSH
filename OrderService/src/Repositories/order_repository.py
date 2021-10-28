from APIModels.order_request_model import OrderRequestModel
from APIModels.credit_card_model import CreditCardModel
from APIModels.order_database_model import OrderDatabaseModel
from Repositories.db_connection import DbConnection


class OrderRepository:
    def __init__(self, connection: DbConnection) -> None:
        self.__connection = connection

    def save_order(self, order: OrderRequestModel) -> int:
        # TODO: save message to persistent storage and return id

        # res_id = self.__connection.execute(
        #     f"""
        #     INSERT INTO message (message) VALUES ('{message.message}') RETURNING id;
        #     """
        # )

        # self.__connection.commit()
        return -1
        # return res_id[0][0]

    # TODO: Ask the typing pervert how to do either OrderModel OR None
    def get_order(self, id: int) -> OrderDatabaseModel:
        # TODO: return message with id from storage
        rows = self.__connection.execute(
            f"""
                SELECT 
                    o.order_id,
                    o.product_id,
                    o.merchant_id,
                    o.buyer_id,
                    c.card_id,
                    c.card_number,
                    c.expiration_month,
                    c.expiration_year,
                    c.cvc,
                    o.discount
                FROM "Order" o
                    INNER JOIN "CreditCard" c ON o.card_id = c.card_id
                WHERE o.order_id = '{id}'
                """
        )

        if len(rows) > 0:
            row = rows[0]
            print("heii")
            print(
                f"Card number: {row[5]}, expiration month: {row[6]}, expiration year: {row[7]}"
            )
            print("beii")

            return OrderDatabaseModel(
                order_id=row[0],
                productId=row[1],
                merchantId=row[2],
                buyerId=row[3],
                creditCard=CreditCardModel(
                    credit_card_id=row[4],
                    cardNumber=row[5],
                    expirationMonth=row[6],
                    expirationYear=row[7],
                    cvc=row[8],
                ),
                discount=row[9],
            )
