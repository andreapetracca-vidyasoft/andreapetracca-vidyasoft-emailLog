from sqlalchemy.orm import Session
from app.pkg.config.DBconnection import connect
from app.pkg.pydantic.Dtos import EmailDTO
from app.pkg.service.Service import EmailService
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/api/internal/emails", tags=["Emails"])


@router.post("/send/v1", status_code=status.HTTP_200_OK)
def send_email(request: EmailDTO, db: Session = Depends(connect)):
    try:
        EmailService(db).Mailsend(request)
        return {"message:": "e-mail inviata con successo"}
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
