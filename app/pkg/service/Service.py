from sqlalchemy.orm import Session
from app.EmailSender import EmailSender
from datetime import datetime, timezone
from app.pkg.repository.LogRepo import LogRepository
from app.pkg.repository.EmailRepo import EmailRepository
from app.pkg.dto.DataClass import EmailDTO, LogDTO, Status
from app.pkg.factory.Factory import insert_email_to_model, insert_log_to_model


PLACEHOLDER = {
    "RESERVE": {
        "subject": "Conferma prenotazione ",
        "body": "Grazie {{nome}} per aver prenotato il libro '{{titoloLibro}}' in data {{data}}.",
    },
    "RETURN": {
        "subject": "Conferma restituzione",
        "body": "Grazie {{nome}} per aver restituito il libro '{{titoloLibro}}'.",
    },
}


class EmailService:

    def __init__(self, db: Session):
        self.db = db
        self.repo1 = EmailRepository(db)
        self.repo2 = LogRepository(db)
        self.sender = EmailSender()

    def select(self, response: str, content: dict) -> str:
        for key, value in content.items():
            response = response.replace(f"{{{{{key}}}}}", str(value))
        return response

    def send(self, payload: EmailDTO) -> None:
        type = payload.email_type.value

        if type not in PLACEHOLDER:
            raise ValueError(f"Tipo email non supportato: {type}")

        response = PLACEHOLDER[type]

        saved = self.repo1.save(insert_email_to_model(payload))

        try:
            self.sender.send(
                to=payload.send_to,
                subject=response["subject"],
                body=self.select(response["body"], payload.fields),
            )
            status = Status.SENT
            error = None

        except Exception as exc:
            status = Status.FAILED
            error = str(exc)

        self.repo2.save(
            insert_log_to_model(
                LogDTO(
                    email_id=saved.id,
                    status=status,
                    error_message=error,
                    created_at=datetime.now(timezone.utc),
                )
            )
        )
