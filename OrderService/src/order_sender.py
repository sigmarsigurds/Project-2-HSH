import pika
from retry import retry

from APIModels.order_database_model import OrderDatabaseModel
from APIModels.order_reservation_model import OrderReservationModel


class OrderSender:
    def __init__(self, rabbitmq_server_host: str) -> None:

        self.rabbitmq_server_host = rabbitmq_server_host
        self.connection = self.__get_connection()
        self.channel = self.connection.channel()

        self.channel.exchange_declare(
            exchange="order-created", exchange_type="direct", durable=True
        )

        # self.channel.queue_declare(queue="order_created_email_queue", durable=True)

    def send_order_email(self, reservation: OrderReservationModel):
        # TODO: send message via rabbitmq

        self.channel.basic_publish(
            exchange="order-created",
            routing_key="order_created_email_queue",
            body=reservation.json(),
            properties=pika.BasicProperties(delivery_mode=2),
        )

        print(f" [x] Sent to EmailService to email the new order '{reservation}'")

    def send_order_payment(self, order: OrderDatabaseModel):
        pass

    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __get_connection(self):
        # TODO: create rabbitmq connection
        return pika.BlockingConnection(
            pika.ConnectionParameters(self.rabbitmq_server_host)
        )
