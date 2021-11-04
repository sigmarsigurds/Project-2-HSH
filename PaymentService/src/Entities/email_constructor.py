from enum import IntEnum

from src.Models import EmailEventModel


class EmailType(IntEnum):
    TRANSACTION_FAILED = 0
    TRANSACTION_SUCCEEDED = 1


class EmailConstructor:
    EMAIL_SUBJECT = {
        0: "Order purchase failed",
        1: "Order has been purchased",
    }

    EMAIL_CONTENT = {
        0: lambda order_id: f"Order {order_id} purchase has failed",
        1: lambda order_id: f"Order {order_id} has been successfully purchased",
    }


    def create_email(self, email_to: str, order_id: int, email_type: EmailType) -> EmailEventModel:

        subject = self.EMAIL_SUBJECT[int(email_type)]
        content = self.EMAIL_CONTENT[int(email_type)](order_id)

        return EmailEventModel(
            email_to=email_to,
            subject=subject,
            content=content
        )
