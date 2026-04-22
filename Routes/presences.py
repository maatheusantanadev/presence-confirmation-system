from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from Database.database import get_db
from Models.presence import Presence
from Models.students import Student
from Models.groups import Group
from Services.presences_service import create_attendance_by_name
from auth import get_current_user
import requests

router = APIRouter(prefix="/presence", tags=["Presences"])


@router.post("")
async def mark_attendance(
        image: UploadFile = File(...),
        group_id: int = Form(...),  # Agora obrigatório vir do front
        db: Session = Depends(get_db)
):
    # 1. Leitura da imagem
    contents = await image.read()
    headers = {"ngrok-skip-browser-warning": "true"}

    # 2. Chamada para a IA Lorena
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

    # 3. Verificação de sucesso da IA
    if not result.get("success"):
        return {"msg": "Aluno não reconhecido"}

    # 4. Extração do nome reconhecido
    student_name_ia = result["usuario"]["nome"]

    # 5. Registro no Banco usando o Service (Passando o group_id)
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
def get_presence_history(
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    user_cpf = current_user.get("cpf")

    # Busca as presenças vinculadas estritamente aos grupos do professor logado
    history = db.query(Presence, Group.name.label("group_name")) \
        .join(Group, Presence.group_id == Group.id) \
        .filter(Group.professor_cpf == user_cpf) \
        .order_by(Presence.date.desc()).all()

    result_dict = {}
    for p, group_name in history:
        if group_name not in result_dict:
            result_dict[group_name] = []

        result_dict[group_name].append({
            "aluno": p.student.name,
            "email": p.student.email,
            "data": p.date.strftime("%d/%m/%Y %H:%M"),
            "status": p.status
        })

    return result_dict