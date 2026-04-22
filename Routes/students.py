from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Database.database import get_db
from Models.students import Student
from Schemas.students import StudentCreate
from Services.studentes_service import create_student
from auth import get_admin_user

router = APIRouter()


@router.get("/students")
def list_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


@router.post("/students")
def create(
        student: StudentCreate,
        db: Session = Depends(get_db),
        admin: dict = Depends(get_admin_user)
):
    try:
        return create_student(
            name=student.name,
            email=student.email,
            registration_number=student.registration_number,  # Argumento que faltava!
            db=db,
            group_id=student.group_id  # Passe o group_id se ele existir no seu Schema
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))