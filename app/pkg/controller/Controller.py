from sqlalchemy.orm import Session
from app.ConnectionDB import connect
from app.pkg.dto.DataClass import EmailDTO
from app.pkg.service.Service import EmailService
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/api/internal/emails", tags=["Emails"])


@router.post("/send/v1", status_code=status.HTTP_200_OK)
def send_email(request: EmailDTO, db: Session = Depends(connect)):
    try:
        EmailService(db).send(request)
        return {"message:": "e-mail inviata con successo"}
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
