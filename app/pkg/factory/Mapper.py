from uuid import uuid4
from datetime import datetime
from app.pkg.model.Orms import Email as EmailModel, Log as LogModel, Type as ModelType
from app.pkg.pydantic.Dtos import EmailDTO, LogDTO, Type as DTOType, Status as DTOStatus


@staticmethod
def model_to_email_dto(email: EmailModel) -> EmailDTO:
    return EmailDTO(
        email_type=DTOType(email.email_type.value),
        send_to=email.send_to,
        fields=email.fields,
        created_at=datetime.now(),
    )


@staticmethod
def insert_email_to_model(email_dto: EmailDTO) -> EmailModel:
    return EmailModel(
        email_type=ModelType(email_dto.email_type.value),
        send_to=email_dto.send_to,
        fields=email_dto.fields,
        created_at=datetime.now(),
    )


@staticmethod
def model_to_log_dto(log: LogModel) -> LogDTO:
    return LogDTO(
        email_id=log.email_id,
        status=DTOStatus(log.status.value),
        error_message=log.error_message,
        created_at=datetime.now(),
    )


@staticmethod
def insert_log_to_model(log_dto: LogDTO) -> LogModel:
    return LogModel(
        id=uuid4(),
        email_id=log_dto.email_id,
        status=DTOStatus(log_dto.status.value),
        error_message=log_dto.error_message,
        created_at=datetime.now(),
    )
