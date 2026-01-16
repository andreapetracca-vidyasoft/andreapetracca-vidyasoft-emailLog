from uuid import UUID
from enum import Enum as ENUM
from datetime import datetime
from app.pkg.config.DBconnection import base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PUUID
from sqlalchemy import CheckConstraint, Enum, JSON, ForeignKey, String, TIMESTAMP, text


class Type(ENUM):
    RESERVE = "RESERVE"
    RETURN = "RETURN"


class Email(base):
    __tablename__ = "emails"

    id: Mapped[UUID] = mapped_column(
        PUUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    email_type: Mapped[Type] = mapped_column(
        Enum(Type, name="email_type_enum"), nullable=False
    )
    send_to: Mapped[str] = mapped_column(String, nullable=False)
    fields: Mapped[dict] = mapped_column(
        JSON, nullable=False, server_default=text("'{}'::json")
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=text("now()")
    )

    __table_args__ = (
        CheckConstraint(
            "send_to ~* '^[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,}$'",
            name="check",
        ),
    )


class Status(ENUM):
    SENT = "SENT"
    FAILED = "FAILED"


class Log(base):
    __tablename__ = "logs"

    id: Mapped[UUID] = mapped_column(
        PUUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    email_id: Mapped[UUID] = mapped_column(
        PUUID(as_uuid=True), ForeignKey("emails.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[Status] = mapped_column(
        Enum(Status, name="status_enum"), nullable=False
    )
    error_message: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=text("now()")
    )
