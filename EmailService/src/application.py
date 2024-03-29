import pika, sys, os
import time
from retry import retry
import json

from email_sender import SendEmail
from email_model import EmailModel


@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def get_connection():
    # TODO: create rabbitmq connection
    return pika.BlockingConnection(pika.ConnectionParameters("rabbitmq", heartbeat=500))


def create_email_model(body):

    return EmailModel(
        emailTo=body.get("email_to"),
        subject=body.get("subject"),
        content=body.get("content"),
    )


user = "honnunproject@gmail.com"
password = "charliesheen14"

email_sender = SendEmail(user, password)


def main():
    connection = get_connection()
    channel = connection.channel()

    channel.exchange_declare(
        exchange="order-created", exchange_type="direct", durable=True
    )
    channel.exchange_declare(
        exchange="payment-processed", exchange_type="direct", durable=True
    )

    channel.queue_declare(queue="send-email-queue", durable=True)

    channel.queue_bind(
        exchange="order-created",
        queue="send-email-queue",
        routing_key="send-email",
    )

    channel.queue_bind(
        exchange="payment-processed", queue="send-email-queue", routing_key="send-email"
    )

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        body = body.decode()  # Body hefur "email_to": "", "subject": "", "content": ""
        email = create_email_model(json.loads(body))
        email_sender.send_email(email)
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="send-email-queue", on_message_callback=callback)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
