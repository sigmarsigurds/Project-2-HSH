import json

import pika, sys, os
import time
from retry import retry

from src.Models import OrderPaymentInformationModel, CreditCardModel, EmailEventModel, InventoryEventModel
from src.Entities import Transaction
from src.Validators import InvalidCreditCard
import src.Entities.email_constructor as email_constructor_file

EmailType = email_constructor_file.EmailType


class TransactionTransceiver:
    def __init__(self,
                 transaction: Transaction,
                 email_constructor: email_constructor_file.EmailConstructor,
                 rabbitmq_server_host: str
                 ):
        self.__connection = self.__get_connection(rabbitmq_server_host)
        self.__channel = self.__connection.channel()
        self.transaction = transaction
        self.__email_constructor = email_constructor

        self.__set_up_receiving_queue()
        self.__set_up_sending_queue()

    @staticmethod
    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __get_connection(rabbitmq_server_host: str):
        # TODO: create rabbitmq connection
        return pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_server_host))

    def __set_up_sending_queue(self):
        self.__channel.exchange_declare(
            exchange="payment-processed",
            exchange_type="direct",
            durable=True
        )

    def __set_up_receiving_queue(self):
        self.__channel.exchange_declare(
            exchange="order-created", exchange_type="direct", durable=True
        )

        self.__channel.queue_declare(queue="order-created-payment-queue", durable=True)

        self.__channel.queue_bind(
            exchange="order-created",
            queue="order-created-payment-queue",
            routing_key="order-created-payment",
        )



        self.__channel.basic_qos(prefetch_count=1)
        self.__channel.basic_consume(
            queue="order-created-payment-queue", on_message_callback=self.__callback
        )

    @staticmethod
    def __create_order_payment_information_model(body: dict):
        credit_card_dict = body.get("credit_card", {})

        print(credit_card_dict)

        credit_card = CreditCardModel(
            card_number=credit_card_dict.get("card_number"),
            expiration_month=credit_card_dict.get("expiration_month"),
            expiration_year=credit_card_dict.get("expiration_year"),
            cvc=credit_card_dict.get("cvc")
        )

        return OrderPaymentInformationModel(
            order_id=body.get("order_id"),
            buyer_email=body.get("buyer_email"),
            merchant_email=body.get("merchant_email"),
            product_id=body.get("product_id"),
            merchant_id=body.get("merchant_id"),
            credit_card=credit_card,
            quantity=body.get("quantity")
        )


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


    @staticmethod
    def __parse_body(body):
        body = body.decode()
        return json.loads(body)


    def __callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body.decode())

        body = self.__parse_body(body)

        order_payment_information = self.__create_order_payment_information_model(body)

        inventory_model = InventoryEventModel(
            product_id=order_payment_information.product_id,
            quantity=order_payment_information.quantity
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
