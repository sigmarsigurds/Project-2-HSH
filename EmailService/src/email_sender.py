from email_model import EmailModel
import yagmail

yag = yagmail.SMTP("honnunproject@gmail.com", "charliesheen14")

yag.send(to="robertingi00@gmail.com", contents="Hello, Mike!")


class SendEmail:
    def __init__(self, user, password):
        self.email_service = yagmail.SMTP(user=user, password=password)

    def send_email(self, email: EmailModel):
        try:
            self.email_service.send(
                to=email.email_to, subject=email.subject, contents=email.content
            )
            print("Email sent successfully")
        except:
            print("Error, email was not sent")
