from .BaseRepo import BaseRepo
from sqlalchemy.orm import Session
from app.pkg.model.Orms import Email


class EmailRepository(BaseRepo):

    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def save(self, record: Email) -> Email:
        return super().save(record)
