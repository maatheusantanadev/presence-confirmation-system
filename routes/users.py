from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        username=user.username,
        password=user.password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    return {"msg": "User criado"}