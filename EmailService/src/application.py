import yagmail
import pika
from retry import retry
from emaill import send_email


@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def get_connection():
    # creating rabbitmq connection
    return pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))


def main():
    connection = get_connection()
    channel = connection.channel()

    channel.exchange_declare(
        exchange="order-created", exchange_type="direct", durable=True
    )

    channel.queue_declare(queue="order_created_email_queue", durable=True)

    channel.queue_bind(
        exchange="order-created",
        queue="order_created_email_queue",
        routing_key="order_created_email_queue",
    )

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        time.sleep(5)
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=email_queue, on_message_callback=callback, auto_ack=True
    )
    channel.start_consuming()


if __name__ == "__main__":
    main()
