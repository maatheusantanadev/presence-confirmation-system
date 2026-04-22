from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from Database.database import get_db
from Models.groups import Group
from Models.presence import Presence
from auth import get_current_user

router = APIRouter(prefix="/stats", tags=["Stats"])

@router.get("")
def get_professor_stats(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Pegamos o CPF do professor logado no token
    user_cpf = current_user.get("cpf")

    # 1. Contagem de Turmas (Total de grupos do professor)
    total_groups = db.query(Group).filter(Group.professor_cpf == user_cpf).count()

    # 2. Contagem de Presenças (Resolvendo a duplicidade)
    # Filtramos as presenças que estão vinculadas a um group_id
    # que pertence a este professor específico.
    total_presences = db.query(Presence).join(
        Group, Presence.group_id == Group.id
    ).filter(
        Group.professor_cpf == user_cpf
    ).count()

    return {
        "total_groups": total_groups,
        "total_presences": total_presences
    }