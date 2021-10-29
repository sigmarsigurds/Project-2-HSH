import pika
from retry import retry

from APIModels.order_database_model import OrderDatabaseModel


class OrderSender:
    def __init__(self, rabbitmq_server_host: str) -> None:
        # TODO: initate connection
        # self.queue_name = queue_name
        self.rabbitmq_server_host = rabbitmq_server_host
        self.connection = self.__get_connection()
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue="order_created_email_queue", durable=True)

    def send_order_email(self, order: OrderDatabaseModel):
        # TODO: send message via rabbitmq

        self.channel.basic_publish(
            exchange="",
            routing_key="order_created_email_queue",
            body=order.json(),
            properties=pika.BasicProperties(delivery_mode=2),
        )

        print(f" [x] Sent to EmailService to email the new order '{order}'")

    def send_order_payment(self, order: OrderDatabaseModel):
        pass

    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __get_connection(self):
        # TODO: create rabbitmq connection
        return pika.BlockingConnection(
            pika.ConnectionParameters(self.rabbitmq_server_host)
        )
