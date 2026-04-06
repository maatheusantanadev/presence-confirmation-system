from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Database.database import get_db
from Models.students import Student
from Schemas.students import StudentCreate
from auth import get_admin_user

router = APIRouter()


@router.get("/students")
def list_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


@router.post("/students")
def create_student(
        student: StudentCreate,
        db: Session = Depends(get_db),
        admin: dict = Depends(get_admin_user)
):
    existing = db.query(Student).filter(Student.email == student.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    db_student = Student(**student.model_dump())

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student