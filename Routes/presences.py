from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from Database.database import get_db
from Models.presence import Presence
from Models.groups import Group
from Services.presences_service import (
    create_attendance_by_name,
    gerar_codigo_turma,
    validar_codigo_turma,
)

router = APIRouter(prefix="/presence", tags=["Presences"])


class GerarCodigoIn(BaseModel):
    group_id: int


class MarcarPresencaIn(BaseModel):
    name: str
    group_id: int
    code: str


@router.post("/code")
def gerar_codigo(payload: GerarCodigoIn, db: Session = Depends(get_db)):
    """
    Gera/renova o código dinâmico de uma turma (uso do professor).
    >>> Proteja com a sua dependência de token (a mesma que protege /stats).
    Ex.: def gerar_codigo(..., user = Depends(get_current_user)):
    """
    try:
        return gerar_codigo_turma(payload.group_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("")
def mark_attendance(payload: MarcarPresencaIn, db: Session = Depends(get_db)):
    """Registra presença SOMENTE se o código dinâmico da turma for válido."""
    # 1) valida o código dinâmico
    try:
        validar_codigo_turma(payload.group_id, payload.code, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 2) registra a presença pelo nome
    try:
        presence, created = create_attendance_by_name(payload.name, payload.group_id, db)
        return {
            "msg": "Presença confirmada!" if created else "Presença já registrada hoje (não duplicada).",
            "created": created,
            "aluno": payload.name,
            "turma_id": payload.group_id,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.get("/history")
def get_presence_history(db: Session = Depends(get_db)):
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