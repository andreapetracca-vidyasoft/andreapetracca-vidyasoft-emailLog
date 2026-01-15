import os
import smtplib
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()


class EmailSender:

    MAIL_HOST = os.getenv("SMTP_HOST", "sandbox.smtp.mailtrap.io")
    MAIL_PORT = int(os.getenv("SMTP_PORT", "2525"))
    MAIL_NAME = str(os.getenv("SMTP_USERNAME"))
    MAIL_PASS = str(os.getenv("SMTP_PASSWORD"))

    SENDER = "Private Person <from@example.com>"

    def send(self, to: str, subject: str, body: str) -> None:
        msg = EmailMessage()
        msg["From"] = self.SENDER
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP(self.MAIL_HOST, self.MAIL_PORT) as server:
            server.login(self.MAIL_NAME, self.MAIL_PASS)
            server.send_message(msg)
