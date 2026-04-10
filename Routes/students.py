from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Database.database import get_db
from Schemas.students import StudentCreate
from Services.student_service import create_student
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
        return create_student(student.name, student.email, db)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))