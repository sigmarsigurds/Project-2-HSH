import json

import pika, sys, os
import time
from retry import retry

from src.Models import InventoryEventModel
from src.Repositories import InventoryRepository


class PaymentQueueReceiving:
    def __init__(self, rabbitmq_server_host: str, inventory_repository: InventoryRepository):
        self.__connection = self.__get_connection(rabbitmq_server_host)
        self.__channel = self.__connection.channel()
        self.__inventory_repository = inventory_repository

        self.__channel.exchange_declare(
            exchange="payment-processed", exchange_type="direct", durable=True
        )

        self.__set_up_payment_failed_queue()
        self.__set_up_payment_succeeded_queue()


    @staticmethod
    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __get_connection(rabbitmq_server_host: str):
        # TODO: create rabbitmq connection
        return pika.BlockingConnection(
            pika.ConnectionParameters(rabbitmq_server_host, heartbeat=500)
        )

    def __set_up_payment_failed_queue(self):
        self.__channel.queue_declare(queue="payment-failed-queue", durable=True)

        self.__channel.queue_bind(
            exchange="payment-processed",
            queue="payment-failed-queue",
            routing_key="payment-failed",
        )

        self.__channel.basic_qos(prefetch_count=1)
        self.__channel.basic_consume(
            queue="payment-failed-queue", on_message_callback=self.__on_payment_failed
        )


    def __set_up_payment_succeeded_queue(self):
        self.__channel.queue_declare(queue="payment-succeeded-queue", durable=True)

        self.__channel.queue_bind(
            exchange="payment-processed",
            queue="payment-succeeded-queue",
            routing_key="payment-succeeded",
        )

        self.__channel.basic_qos(prefetch_count=1)
        self.__channel.basic_consume(
            queue="payment-succeeded-queue", on_message_callback=self.__on_payment_succeeded
        )


    @staticmethod
    def __event_finished(ch, method):
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)


    @staticmethod
    def __create_inventory_event_model(body: dict):
        return InventoryEventModel(
            product_id=body.get("product_id"),
            quantity=body.get("quantity")
        )


    @staticmethod
    def __parse_body(body):
        body = body.decode()
        return json.loads(body)

    def __on_payment_failed(self, ch, method, properties, body):
        print("Payment failed")

        body = self.__parse_body(body)

        inventory_event_model = self.__create_inventory_event_model(body)

        print(inventory_event_model)

        self.__inventory_repository.free_reserved_product(
            inventory_event_model.product_id,
            inventory_event_model.quantity
        )

        self.__event_finished(ch, method)  # This could be done with decorator


    def __on_payment_succeeded(self, ch, method, properties, body):
        print("Payment succeeded")
        print(body.decode())

        body = self.__parse_body(body)

        inventory_event_model = self.__create_inventory_event_model(body)

        self.__inventory_repository.sell_product(
            inventory_event_model.product_id,
            inventory_event_model.quantity
        )

        self.__event_finished(ch, method)  # This could be done with decorator


    def start(self):
        print(" [*] Waiting for messages. To exit press CTRL+C")
        self.__channel.start_consuming()


