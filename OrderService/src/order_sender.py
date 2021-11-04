import pika
from retry import retry

from APIModels.order_database_model import OrderDatabaseModel
from APIModels.order_email_information_model import OrderEmailInformationModel
from APIModels.order_payment_information_model import OrderPaymentInformationModel
from APIModels.email_model import EmailModel


class OrderSender:
    def __init__(self, rabbitmq_server_host: str) -> None:

        self.rabbitmq_server_host = rabbitmq_server_host
        self.connection = self.__get_connection()
        self.channel = self.connection.channel()

        self.channel.exchange_declare(
            exchange="order-created", exchange_type="direct", durable=True
        )

        # self.channel.queue_declare(queue="order_created_email_queue", durable=True)

    def send_order_email(self, order_email_information: OrderEmailInformationModel):

        subject = "Order has been created"
        content = f"""
        <h1 style='text-align: center;margin-bottom: .3rem;font-stretch: expanded'>Order has been created</h1>
        <h2 style='text-align: center;font-style: italic;font-weight: normal'>Order: {order_email_information.order_id}</h2>
        <ul style='margin-left: 3rem;list-style-type: none'>
            <li style='font-size: 1.2rem'>Product: {order_email_information.product_name}</li>
            <li style='font-size: 1.2rem'>Total Price: ${order_email_information.order_price}</li>
        </ul>
        """
        # content = f"<h1>Order:</h1> {order_email_information.order_id}\nProduct: {order_email_information.product_name}\nPrice: {order_email_information.order_price}"

        # Send to merchant
        self.__send_email(
            recepient=order_email_information.merchant_email,
            subject=subject,
            content=content,
        )

        # Send to buyer
        self.__send_email(
            recepient=order_email_information.buyer_email,
            subject=subject,
            content=content,
        )

    def send_order_payment(
        self, order_payment_information: OrderPaymentInformationModel
    ):
        self.channel.basic_publish(
            exchange="order-created",
            routing_key="order-created-payment-queue",
            body=order_payment_information.json(),
            properties=pika.BasicProperties(delivery_mode=2),
        )
        print(
            f" [x] Sent to PaymentService the new order '{order_payment_information}'"
        )

    def __send_email(self, recepient: str, subject: str, content: str):
        # Send to merchant
        self.channel.basic_publish(
            exchange="order-created",
            routing_key="send-email",
            body=EmailModel(emailTo=recepient, subject=subject, content=content).json(),
            properties=pika.BasicProperties(delivery_mode=2),
        )

        print(f" [x] Sent to EmailService ({recepient}) the new order")

    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __get_connection(self):
        # TODO: create rabbitmq connection
        return pika.BlockingConnection(
            pika.ConnectionParameters(self.rabbitmq_server_host, heartbeat=5)
        )
