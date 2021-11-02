import yagmail
import pika
from retry import retry
from emaill import send_email


@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def get_connection():
    # creating rabbitmq connection
    return pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))


# send_email()


if __name__ == "__main__":

    connection = get_connection()
    channel = connection.channel()

    channel.exchange_declare(exchange="emails", exchange_type="fanout")

    result = channel.queue_declare(queue="", exclusive=True)
    email_queue = result.method.queue

    channel.queue_bind(exchange="emails", queue=email_queue)
    print(" [*] Waiting for email. To exit press CTRL+C")

    def callback(body):
        print("it work")

    channel.basic_consume(
        queue=email_queue, on_message_callback=callback, auto_ack=True
    )
    channel.start_consuming()
