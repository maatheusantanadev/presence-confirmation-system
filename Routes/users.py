from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from Database.database import get_db
from Models.user import User  # Certifique-se que o nome do arquivo/classe está correto
from Schemas.user import UserCreate
from Utils.utils import hash_password, verify_password
from auth import create_token, get_admin_user

router = APIRouter(tags=["Users"])


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # 1. Verifica se o Username já existe
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username já existe")

    # 2. Verifica se o CPF já está cadastrado
    if db.query(User).filter(User.cpf == user.cpf).first():
        raise HTTPException(status_code=400, detail="Este CPF já está vinculado a outra conta")

    hashed_pw = hash_password(user.password)

    # 3. Cria o usuário com os novos campos e Role fixo
    db_user = User(
        full_name=user.full_name,
        cpf=user.cpf,
        username=user.username.lower(),
        password=hashed_pw,
        role="admin"  # Definido internamente, removido do Schema
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"msg": "Professor cadastrado com sucesso", "username": db_user.username}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao salvar: {str(e)}")


@router.post("/login")
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username.lower()).first()

    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Senha incorreta")

    # Incluímos o CPF no token para facilitar buscas no frontend
    token = create_token({
        "sub": user.username,
        "role": user.role,
        "cpf": user.cpf
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_cpf": user.cpf  # Retornamos o CPF para o localStorage do JS
    }


@router.post("/logout")
def logout():
    return {"msg": "Logout realizado com sucesso"}


@router.delete("/{user_id}")
def delete_user(
        user_id: int,
        db: Session = Depends(get_db),
        admin: dict = Depends(get_admin_user)
):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if admin["sub"] == db_user.username:
        raise HTTPException(status_code=400, detail="Você não pode deletar sua própria conta")

    db.delete(db_user)
    db.commit()

    return {"msg": f"Usuário {db_user.username} deletado"}