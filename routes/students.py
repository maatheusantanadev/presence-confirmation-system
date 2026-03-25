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

#Putin

@router.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted"}