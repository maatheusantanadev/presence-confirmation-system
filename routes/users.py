from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate
from util import hash_password, verify_password
from auth import create_token, get_admin_user

router = APIRouter()

# REGISTRAR USUÁRIO
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    # Normaliza username (evita duplicidade tipo "Pedro" e "pedro")
    username = user.username.lower()

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
    # Logout é controlado pelo cliente (frontend)
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

    # Verifica se existe
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Evita que o admin delete a si mesmo
    if admin["sub"] == db_user.username:
        raise HTTPException(status_code=400, detail="Não pode deletar a si mesmo")

    # Remove do banco
    db.delete(db_user)
    db.commit()

    return {"msg": "Usuário deletado com sucesso"}
