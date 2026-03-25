from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Student
from schemas import StudentCreate

router = APIRouter()

@router.get("/students")
def list_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@router.post("/students")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    return db_student

@router.put("/students/{student_id}")
def update_student(
    student_id: int,
    data: StudentCreate,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        return {"error": "Aluno não encontrado"}

    student.name = data.name
    student.email = data.email

    db.commit()
    db.refresh(student)

    return student

@router.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted"}