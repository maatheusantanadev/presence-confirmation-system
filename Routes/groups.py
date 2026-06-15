from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from Database.database import get_db
from Models.groups import Group
from Schemas.groups import GroupCreate, GroupResponse
from Services.groups_services import create_group
from auth import get_current_user

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.post("", response_model=GroupResponse)
def make_group(
        group: GroupCreate,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    try:
        return create_group(
            group.name,
            current_user["cpf"],
            group.student_registration_numbers,
            db
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[GroupResponse])
def list_groups(
        db: Session = Depends(get_db)
):
    return db.query(Group).all()


@router.get("/{group_id}", response_model=GroupResponse)
def get_group_details(
        group_id: int,
        db: Session = Depends(get_db)
):
    group = db.query(Group).filter(Group.id == group_id).first()

    if not group:
        raise HTTPException(status_code=404, detail="Turma não encontrada")

    return group