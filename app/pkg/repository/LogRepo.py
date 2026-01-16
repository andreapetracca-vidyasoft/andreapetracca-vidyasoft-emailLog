from .BaseRepo import BaseRepo
from app.pkg.model.Orms import Log
from sqlalchemy.orm import Session


class LogRepository(BaseRepo):

    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def save(self, record: Log) -> Log:
        return super().save(record)
