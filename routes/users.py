from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate
from utils import hash_password, verify_password
from auth import create_token, get_admin_user
import re

router = APIRouter()

# Funções auxiliares de validação
def validate_username(username: str):
    if len(username) < 3:
        raise HTTPException(status_code=422, detail="Username muito curto")
    if len(username) > 20:
        raise HTTPException(status_code=422, detail="Username muito longo")

def validate_password(password: str):
    if len(password) < 6:
        raise HTTPException(status_code=422, detail="Senha muito curta")
    if not re.search(r"\d", password):
        raise HTTPException(status_code=422, detail="Senha deve conter ao menos um número")

def validate_role(role: str):
    if not role or role.strip() == "":
        raise HTTPException(status_code=422, detail="Role não pode estar vazio")


# REGISTRAR USUÁRIO
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    # Normaliza username (evita duplicidade tipo "Pedro" e "pedro")
    username = user.username.lower()

    # Valida inputs
    validate_username(username)
    validate_password(user.password)
    validate_role(user.role)

    # Verifica se o username já existe
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username já existe")

    # Gera hash da senha
    hashed_password = hash_password(user.password)

    # Cria usuário
    db_user = User(
        username=username,
        password=hashed_password,
        role=user.role
    )

    # Salva no banco
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"msg": "User criado"}


# LOGIN
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    # Busca usuário
    user = db.query(User).filter(User.username == form_data.username.lower()).first()

    # Valida usuário
    if not user:
        raise HTTPException(status_code=401, detail="Usuário inválido")

    # Valida senha
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Senha inválida")

    # Gera token
    token = create_token({
        "sub": user.username,
        "role": user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# LOGOUT
@router.post("/logout")
def logout():
    return {"msg": "Logout feito (cliente deve apagar token)"}


# DELETAR USUÁRIO
@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_admin_user)
):

    # Busca usuário
    db_user = db.query(User).filter_by(id=user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if admin["sub"] == db_user.username:
        raise HTTPException(status_code=400, detail="Não pode deletar a si mesmo")

    db.delete(db_user)
    db.commit()

    return {"msg": "Usuário deletado com sucesso"}