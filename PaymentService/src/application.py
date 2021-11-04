import pika, sys, os
import time
from retry import retry


@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def get_connection():
    # TODO: create rabbitmq connection
    return pika.BlockingConnection(pika.ConnectionParameters("rabbitmq", heartbeat=5))


def main():
    connection = get_connection()
    channel = connection.channel()

    channel.exchange_declare(
        exchange="order-created", exchange_type="direct", durable=True
    )

    channel.queue_declare(queue="order_created_payment_queue", durable=True)

    channel.queue_bind(
        exchange="order-created",
        queue="order_created_payment_queue",
        routing_key="order_created_payment_queue",
    )

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        time.sleep(5)
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue="order_created_payment_queue", on_message_callback=callback
    )

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    main()
