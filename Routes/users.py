from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from Database.database import get_db
from Models.user import User
from Schemas.user import UserCreate
from Utils.utils import hash_password, verify_password
from auth import create_token, get_admin_user
import re

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username já existe")

    hashed_password = hash_password(user.password)

    db_user = User(
        username=user.username,
        password=hashed_password,
        role=user.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"msg": "User criado"}


@router.post("/login")
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username.lower()).first()

    if not user:
        raise HTTPException(status_code=401, detail="Usuário inválido")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Senha inválida")

    token = create_token({
        "sub": user.username,
        "role": user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout():
    return {"msg": "Logout feito (cliente deve apagar token)"}


@router.delete("/{user_id}")
def delete_user(
        user_id: int,
        db: Session = Depends(get_db),
        admin: dict = Depends(get_admin_user)
):
    db_user = db.query(User).filter_by(id=user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if admin["sub"] == db_user.username:
        raise HTTPException(status_code=400, detail="Não pode deletar a si mesmo")

    db.delete(db_user)
    db.commit()

    return {"msg": "Usuário deletado com sucesso"}
