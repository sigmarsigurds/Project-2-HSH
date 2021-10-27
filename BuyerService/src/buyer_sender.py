import pika
from retry import retry


class BuyerSender:
    def __init__(self) -> None:
        # initate connection
        connection = self.__get_connection()
        self.channel = connection.channel()
        self.channel.exchange_declare(exchange="buyers", exchange_type="fanout")

    def send_buyer(self, buyer):
        self.channel.basic_publish(
            exchange="buyers", routing_key="", body=buyer.name
        )  # TODO: breyta því body er bara buyer name
        print(" [x] Sent %r" % buyer.name)

    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __get_connection(self):
        # create rabbitmq connection
        return pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
