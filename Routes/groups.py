from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from Database.database import get_db
from Models.groups import Group
from Schemas.groups import GroupCreate, GroupResponse
from Services.groups_services import create_group
from auth import get_current_user

router = APIRouter(prefix="/groups", tags=["Groups"])


# 1. CRIAR TURMA (Você já tem)
@router.post("", response_model=GroupResponse)
def make_group(
        group: GroupCreate,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    try:
        return create_group(group.name, group.professor_cpf, group.student_registration_numbers, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# 2. LISTAR TURMAS DO PROFESSOR LOGADO
@router.get("", response_model=List[GroupResponse])
def list_my_groups(
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    # Buscamos as turmas onde o professor_cpf é igual ao CPF do usuário logado
    # Note: O seu get_current_user deve retornar o CPF ou username no dict
    user_cpf = current_user.get("cpf")

    groups = db.query(Group).filter(Group.professor_cpf == user_cpf).all()
    return groups


# 3. VER DETALHES DE UMA TURMA ESPECÍFICA (Com Alunos)
@router.get("/{group_id}", response_model=GroupResponse)
def get_group_details(
        group_id: int,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    group = db.query(Group).filter(Group.id == group_id).first()

    if not group:
        raise HTTPException(status_code=404, detail="Turma não encontrada")

    # Verifica se a turma pertence ao professor logado
    if group.professor_cpf != current_user.get("cpf"):
        raise HTTPException(status_code=403, detail="Acesso negado a esta turma")

    return group