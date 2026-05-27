from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import re

from Database.database import get_db
from Models.user import User
from Schemas.user import UserCreate
from Utils.utils import hash_password, verify_password
from auth import create_token, get_admin_user

router = APIRouter(tags=["Users"])


# =========================
# LISTAR USUÁRIOS
# =========================
@router.get("/users")
def list_users(
    db: Session = Depends(get_db),
):
    users = db.query(User).all()

    return [
        {
            "id": user.id,
            "full_name": user.full_name,
            "cpf": user.cpf,
            "username": user.username,
            "role": user.role
        }
        for user in users
    ]


# =========================
# REGISTRO
# =========================
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        # Remove qualquer máscara do CPF
        cpf_clean = re.sub(r"\D", "", user.cpf)

        # Validação básica do CPF
        if len(cpf_clean) != 11:
            raise HTTPException(
                status_code=400,
                detail="CPF inválido"
            )

        # Username sempre minúsculo
        username_clean = user.username.strip().lower()

        # Verifica username existente
        existing_username = db.query(User).filter(
            User.username == username_clean
        ).first()

        if existing_username:
            raise HTTPException(
                status_code=400,
                detail="Username já existe"
            )

        # Verifica CPF existente
        existing_cpf = db.query(User).filter(
            User.cpf == cpf_clean
        ).first()

        if existing_cpf:
            raise HTTPException(
                status_code=400,
                detail="Este CPF já está vinculado a outra conta"
            )

        # Hash da senha
        hashed_pw = hash_password(user.password)

        # Criação do usuário
        db_user = User(
            full_name=user.full_name.strip(),
            cpf=cpf_clean,
            username=username_clean,
            password=hashed_pw,
            role="teacher"
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return {
            "msg": "Professor cadastrado com sucesso",
            "user": {
                "id": db_user.id,
                "full_name": db_user.full_name,
                "cpf": db_user.cpf,
                "username": db_user.username,
                "role": db_user.role
            }
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()

        print(f"Erro ao registrar usuário: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Erro interno ao cadastrar usuário"
        )


# =========================
# LOGIN
# =========================
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    try:
        username = form_data.username.strip().lower()

        user = db.query(User).filter(
            User.username == username
        ).first()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Usuário não encontrado"
            )

        if not verify_password(form_data.password, user.password):
            raise HTTPException(
                status_code=401,
                detail="Senha incorreta"
            )

        # Criação do token JWT
        token = create_token({
            "sub": user.username,
            "role": user.role,
            "cpf": user.cpf
        })

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "cpf": user.cpf,
                "username": user.username,
                "role": user.role
            }
        }

    except HTTPException:
        raise

    except Exception as e:
        print(f"Erro no login: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Erro interno ao realizar login"
        )


# =========================
# LOGOUT
# =========================
@router.post("/logout")
def logout():
    return {
        "msg": "Logout realizado com sucesso"
    }


# =========================
# DELETAR USUÁRIO
# =========================
@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_admin_user)
):
    try:
        db_user = db.query(User).filter(
            User.id == user_id
        ).first()

        if not db_user:
            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado"
            )

        # Impede admin de deletar a si próprio
        if admin["sub"] == db_user.username:
            raise HTTPException(
                status_code=400,
                detail="Você não pode deletar sua própria conta"
            )

        db.delete(db_user)
        db.commit()

        return {
            "msg": f"Usuário {db_user.username} deletado com sucesso"
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()

        print(f"Erro ao deletar usuário: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Erro interno ao deletar usuário"
        )