from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from Database.database import get_db
from Models.presence import Presence
from Models.groups import Group
from Services.presences_service import create_attendance_by_name
import requests

router = APIRouter(prefix="/presence", tags=["Presences"])


@router.post("")
async def mark_attendance(
        image: UploadFile = File(...),
        group_id: int = Form(...),
        db: Session = Depends(get_db)
):
    contents = await image.read()
    headers = {"ngrok-skip-browser-warning": "true"}

    try:
        response = requests.post(
            "https://unpoetically-stampedable-lorena.ngrok-free.dev/reconhecer",
            files={"file": ("face.jpg", contents, "image/jpeg")},
            headers=headers,
            timeout=15
        )
        result = response.json()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Erro na IA: {str(e)}")

    if not result.get("success"):
        return {"msg": "Aluno não reconhecido"}

    student_name_ia = result["usuario"]["nome"]

    try:
        create_attendance_by_name(student_name_ia, group_id, db)
        return {
            "msg": "Presença confirmada!",
            "aluno": student_name_ia,
            "turma_id": group_id
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.get("/history")
def get_presence_history(db: Session = Depends(get_db)):
    try:
        history = db.query(Presence, Group.name.label("group_name")) \
            .join(Group, Presence.group_id == Group.id) \
            .order_by(Presence.date.desc()).all()

        result_dict = {}
        for p, group_name in history:
            if not p.student:
                continue
            result_dict.setdefault(group_name, []).append({
                "aluno": p.student.name,
                "email": p.student.email,
                "data": p.date.strftime("%d/%m/%Y %H:%M") if p.date else "",
                "status": p.status
            })
        return result_dict

    except Exception as e:
        import traceback
        return {"DEBUG_ERRO": str(e), "trace": traceback.format_exc()}