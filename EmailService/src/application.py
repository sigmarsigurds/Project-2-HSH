import pika, sys, os
import time
from retry import retry

from emaill import EmailSender
from email_model import EmailModel


@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def get_connection():
    # TODO: create rabbitmq connection
    return pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))


def create_email_model(body):
    return EmailModel(
        email_to=body.email_to,
        subject=body.subject,
        content=body.content,
    )


user = "honnunproject@gmail.com"
password = "charliesheen14"

email_sender = EmailSender(user, password)


def main():
    print("getting connection")
    connection = get_connection()
    print("got connection")
    channel = connection.channel()

    channel.queue_declare(queue="order_created_email_queue", durable=True)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        body = body.decode()  # Body hefur "email_to": "", "subject": "", "content": ""
        email = create_email_model(body)
        email_sender.send_email(email)
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue="order_created_email_queue", on_message_callback=callback
    )

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
