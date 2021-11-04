import pika, sys, os
import time
from retry import retry

from src.Models import OrderPaymentInformationModel, CreditCardModel, EmailEventModel, InventoryEventModel
from src.Entities import Transaction
from src.Validators import InvalidCreditCard
from src.Entities import EmailConstructor, EmailType


class TransactionTransceiver:
    def __init__(self,
                 transaction: Transaction,
                 email_constructor: EmailConstructor,
                 rabbitmq_server_host: str
                 ):
        self.__connection = self.__get_connection
        self.__channel = self.__connection.channel()
        self.transaction = transaction
        self.__email_constructor = email_constructor


        self.__set_up_receiving_queue()
        self.__set_up_sending_queue()

    @staticmethod
    def __create_order_payment_information_model(body: dict):

        credit_card_dict = body.get("creditCard", {})

        credit_card = CreditCardModel(
            cardNumer=credit_card_dict.get("cardNumber"),
            expiration_month=credit_card_dict.get("expirationMonth"),
            expiration_year=credit_card_dict.get("expirationYear"),
            csv=credit_card_dict.get("cvc")
        )

        return OrderPaymentInformationModel(
            orderId=body.get("orderId"),
            buyerEmail=body.get("buyerEmail"),
            merchantEmail=body.get("merchantEmail"),
            productId=body.get("productId"),
            merchantId=body.get("merchantId"),
            creaditCard=credit_card
        )


    def __set_up_sending_queue(self):
        self.__channel.exchange_declare(
            exchange="payment-processed",
            exchange_type="direct",
            durable=True  # Not broken
        )


    def __set_up_receiving_queue(self):
        self.__channel.exchange_declare(
            exchange="order-created", exchange_type="direct", durable=True
        )

        self.__channel.queue_declare(queue="order_created_payment_queue", durable=True)

        self.__channel.queue_bind(
            exchange="order-created",
            queue="order_created_payment_queue",
            routing_key="order_created_payment_queue",
        )

        self.__channel.basic_qos(prefetch_count=1)
        self.__channel.basic_consume(
            queue="order_created_payment_queue", on_message_callback=self.__callback
        )


    @staticmethod
    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __get_connection(rabbitmq_server_host: str):
        # TODO: create rabbitmq connection
        return pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_server_host))


    def __transaction_failed(self, inventory_model: InventoryEventModel, order_id, customer_email, merchant_email):
        # Send transaction status mail
        self.__channel.basic_publish(
            exchange="payment-processed",
            routing_key="payment-failed-queue",
            body=inventory_model.json(),
        )

        # Create email to send to customer and merchant
        email_to_customer = self.__email_constructor.create_email(
            customer_email, order_id, EmailType.TRANSACTION_FAILED)

        email_to_merchant = self.__email_constructor.create_email(
            merchant_email, order_id, EmailType.TRANSACTION_FAILED)

        self.__send_email(email_to_customer)
        self.__send_email(email_to_merchant)


    def __transaction_succeeded(self, inventory_model: InventoryEventModel, order_id, customer_email, merchant_email):
        # Send transaction succeeded event

        # Send transaction status mail
        self.__channel.basic_publish(
            exchange="payment-processed",
            routing_key="payment-success-queue",
            body=inventory_model.json(),
        )

        # Create email to send to customer and merchant
        email_to_customer = self.__email_constructor.create_email(
            customer_email, order_id, EmailType.TRANSACTION_FAILED)

        email_to_merchant = self.__email_constructor.create_email(
            merchant_email, order_id, EmailType.TRANSACTION_FAILED)

        self.__send_email(email_to_customer)
        self.__send_email(email_to_merchant)


    def __send_email(self, email_model: EmailEventModel):
        self.__channel.basic_publish(
            exchange="payment-processed",
            routing_key="send-email-queue",
            body=email_model.json(),
        )


    def __callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        order_payment_information = self.__create_order_payment_information_model(body)

        inventory_model = InventoryEventModel(
            order_payment_information.product_id,
            order_payment_information.quantity
        )

        order_id = order_payment_information.order_id
        customer_email = order_payment_information.buyer_email
        merchant_email = order_payment_information.merchant_email

        try:
            self.transaction.preform_transaction(order_payment_information)

        except InvalidCreditCard:
            self.__transaction_failed(inventory_model, order_id, customer_email, merchant_email)

        del order_payment_information.credit_card  # So credit_card will not be sent by accident
        self.__transaction_succeeded(inventory_model, order_id, customer_email, merchant_email)

        time.sleep(5)
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)


    def start(self):
        print(" [*] Waiting for messages. To exit press CTRL+C")
        self.__channel.start_consuming()







