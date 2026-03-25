from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models import Presence
from datetime import datetime
import requests

router = APIRouter()

@router.post("/presence")
def mark_attendance(
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    response = requests.post(
        "https://unpoetically-stampedable-lorena.ngrok-free.dev/reconhecer",
        files={"file": image.file}
    )

    result = response.json()

    if not result.get("success"):
        return {"msg": "Aluno não reconhecido"}

    student_id = result["usuario"]["id"]

    attendance = Presence(
        student_id=student_id,
        date=datetime.utcnow(),
        status="presente"
    )

    db.add(attendance)
    db.commit()

    return {"msg": "Presença confirmada"}