import pika
from retry import retry

from APIModels.order_database_model import OrderDatabaseModel


class OrderSender:
    def __init__(self, queue_name: str, rabbitmq_server: str) -> None:
        # TODO: initate connection
        self.queue_name = queue_name
        self.rabbitmq_server = rabbitmq_server
        self.connection = self.__get_connection()
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)

    def send_order(self, order: OrderDatabaseModel):
        # TODO: send message via rabbitmq

        self.channel.basic_publish(exchange="", routing_key=self.queue_name, body=order)

        print(f" [x] Sent '{order}'")

    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __get_connection(self):
        # TODO: create rabbitmq connection
        return pika.BlockingConnection(pika.ConnectionParameters(self.rabbitmq_server))
