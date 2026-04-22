from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from Database.database import get_db
from Models.groups import Group
from Models.presence import Presence
from Models.associations import group_members
from auth import get_current_user

router = APIRouter(prefix="/stats", tags=["Stats"])

@router.get("")
def get_professor_stats(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_cpf = current_user.get("cpf")

    # 1. Total de turmas do professor
    total_groups = db.query(Group).filter(Group.professor_cpf == user_cpf).count()

    # 2. Total de presenças confirmadas nas turmas deste professor
    # Fazemos um Join: Presença -> Aluno -> Tabela de Associação -> Turma
    total_presences = db.query(func.count(Presence.id))\
        .join(Presence.student)\
        .join(group_members, Presence.student_id == group_members.c.student_id)\
        .join(Group, group_members.c.group_id == Group.id)\
        .filter(Group.professor_cpf == user_cpf)\
        .scalar()

    return {
        "total_groups": total_groups,
        "total_presences": total_presences or 0
    }