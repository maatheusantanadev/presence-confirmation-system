from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from Database.database import get_db
from Models.presence import Presence
from Models.students import Student
from Models.groups import Group
from Models.associations import group_members
from Services.presences_service import create_attendance_by_name
from auth import get_current_user
import requests

router = APIRouter(prefix="/presence", tags=["Presences"])

@router.post("")
async def mark_attendance(image: UploadFile = File(...), db: Session = Depends(get_db)):
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
        return {"msg": f"Erro de conexão com a IA: {str(e)}"}

    if not result.get("success"):
        return {"msg": "Aluno não reconhecido pela IA"}

    # Captura o nome retornado pela Lorena
    student_name_ia = result["usuario"]["nome"]

    try:
        # O Service agora busca pelo nome e vincula ao ID local correto
        create_attendance_by_name(student_name_ia, db)
        return {"msg": "Presença confirmada!", "aluno": student_name_ia}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/history")
def get_presence_history(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_cpf = current_user.get("cpf")

    # OTIMIZAÇÃO: Buscamos a presença e o nome da turma em um único JOIN
    # Assim não precisamos fazer 50 queries se houver 50 presenças
    history = db.query(
        Presence,
        Group.name.label("group_name")
    ).join(Student, Presence.student_id == Student.id)\
     .join(group_members, Student.id == group_members.c.student_id)\
     .join(Group, group_members.c.group_id == Group.id)\
     .filter(Group.professor_cpf == user_cpf)\
     .order_by(Group.name, Presence.date.desc()).all()

    # Agrupando os dados para o formato que o seu Frontend (Presencas.js) espera
    result = {}
    for p, group_name in history:
        if group_name not in result:
            result[group_name] = []

        result[group_name].append({
            "aluno": p.student.name,
            "data": p.date.strftime("%d/%m/%Y %H:%M"),
            "status": p.status
        })

    return result