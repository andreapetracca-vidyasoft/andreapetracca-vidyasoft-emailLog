from typing import Generic, TypeVar

T = TypeVar("T")


class BaseRepo(Generic[T]):
    def __init__(self, db) -> None:
        self.db = db

    def save(self, record: T) -> T:
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record
