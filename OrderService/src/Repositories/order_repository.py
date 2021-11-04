from APIModels.order_request_model import OrderRequestModel
from APIModels.credit_card_model import CreditCardModel
from APIModels.order_database_model import OrderDatabaseModel
from APIModels.product_model import ProductModel
from Tools.FormatCreditCardNumber import FormatCreditCardNumber
from Repositories.db_connection import DbConnection


class OrderRepository:
    def __init__(self, connection: DbConnection) -> None:
        self.__connection = connection

    def save_order(
        self, order: OrderRequestModel, product: ProductModel
    ) -> OrderDatabaseModel:

        # credit_card_results = self.__connection.execute(
        #     f"""
        #     INSERT INTO "CreditCard" (card_id, card_number, expiration_month, expiration_year, cvc)
        #     VALUES (
        #             DEFAULT,
        #             {order.credit_card.card_number},
        #             {order.credit_card.expiration_month},
        #             {order.credit_card.expiration_year},
        #             {order.credit_card.cvc}
        #             )
        #     RETURNING card_id, card_number, expiration_month, expiration_year, cvc;
        #     """
        # )
        card_number = FormatCreditCardNumber.format(order.credit_card.card_number)
        total_price = (
            float(product.price)
            if order.discount is None or order.discount == 0
            else float(product.price) * float(order.discount)
        )
        order = self.__connection.execute(
            f"""
            INSERT INTO "Order" (order_id, product_id, merchant_id, buyer_id, card_number, total_price) 
            VALUES (
                    DEFAULT, 
                    {order.product_id}, 
                    {order.merchant_id},
                    {order.buyer_id},
                    '{card_number}',
                    {total_price}
                    )
            RETURNING order_id, product_id, merchant_id, buyer_id, card_number, total_price;
            """
        )
        return OrderDatabaseModel(
            orderId=order[0][0],
            productId=order[0][1],
            merchantId=order[0][2],
            buyerId=order[0][3],
            cardNumber=order[0][4],
            totalPrice=order[0][5],
        )

    def get_order(self, id: int) -> OrderDatabaseModel:

        rows = self.__connection.execute(
            f"""
                SELECT 
                    order_id,
                    product_id,
                    merchant_id,
                    buyer_id,
                    card_number,
                    total_price
                FROM "Order" 
                WHERE order_id = '{id}'
                """
        )

        if len(rows) > 0:
            row = rows[0]

            return OrderDatabaseModel(
                orderId=row[0],
                productId=row[1],
                merchantId=row[2],
                buyerId=row[3],
                cardNumber=row[4],
                totalPrice=row[5],
            )
