import pika
from retry import retry


@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def get_connection():
    # TODO: create rabbitmq connection
    return pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))


def callback(name, ssn, email, phonenumber):
    print(" [x] %r" % name)


if __name__ == "__main__":
    # TODO: consume message events and print them to console

    connection = get_connection()
    channel = connection.channel()

    channel.exchange_declare(exchange="buyers", exchange_type="fanout")

    result = channel.queue_declare(queue="", exclusive=True)
    buyer_queue = result.method.queue

    channel.queue_bind(exchange="buyers", queue=buyer_queue)
    print(" [*] Waiting for messages. To exit press CTRL+C")

    channel.basic_consume(
        queue=buyer_queue, on_message_callback=callback, auto_ack=True
    )
    channel.start_consuming()
