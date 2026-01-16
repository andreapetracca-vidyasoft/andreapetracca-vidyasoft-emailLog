import os
import json
import smtplib
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from email.message import EmailMessage
from datetime import datetime, timezone
from app.pkg.repository.LogRepo import LogRepository
from app.pkg.repository.EmailRepo import EmailRepository
from app.pkg.pydantic.Dtos import EmailDTO, LogDTO, Status
from app.pkg.factory.Mapper import insert_email_to_model, insert_log_to_model

load_dotenv()

JSON_PATH = Path(__file__).resolve().parent / "templates.json"


class EmailService:

    SMTP_HOST = os.getenv("SMTP_HOST", "sandbox.smtp.mailtrap.io")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "2525"))
    SMTP_USER = str(os.getenv("SMTP_USERNAME"))
    SMTP_PASS = str(os.getenv("SMTP_PASSWORD"))
    SENDER = "Private <noreply@example.com>"

    def __init__(self, db: Session):
        self.db = db
        self.repo1 = EmailRepository(db)
        self.repo2 = LogRepository(db)
        self.templates = self.load()

    @staticmethod
    def load() -> dict:
        with open(JSON_PATH, encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def render(template: str, fields: dict) -> str:
        for key, value in fields.items():
            template = template.replace(f"{{{{{key}}}}}", str(value))
        return template

    def SMPTsend(self, to: str, subject: str, body: str) -> None:
        msg = EmailMessage()
        msg["From"] = self.SENDER
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP(self.SMTP_HOST, self.SMTP_PORT) as server:
            server.login(self.SMTP_USER, self.SMTP_PASS)
            server.send_message(msg)

    def Mailsend(self, payload: EmailDTO) -> None:
        type = payload.email_type.value

        if type not in self.templates:
            raise ValueError(f"Tipo email non supportato: {type}")

        template = self.templates[type]

        model = self.repo1.save(insert_email_to_model(payload))

        try:
            self.SMPTsend(
                to=payload.send_to,
                subject=template["subject"],
                body=self.render(template["body"], payload.fields),
            )
            status = Status.SENT
            error = None

        except Exception as exc:
            status = Status.FAILED
            error = str(exc)

        self.repo2.save(
            insert_log_to_model(
                LogDTO(
                    email_id=model.id,
                    status=status,
                    error_message=error,
                    created_at=datetime.now(timezone.utc),
                )
            )
        )
