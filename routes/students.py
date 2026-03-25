from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Student
from schemas import StudentCreate
from auth import get_admin_user

router = APIRouter()

# LISTAR ALUNOS
@router.get("/students")
def list_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

# CRIAR ALUNO
@router.post("/students")
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_admin_user)
):
    # Verifica se já existe um aluno com o mesmo email
    existing = db.query(Student).filter(Student.email == student.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    db_student = Student(**student.dict())

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student

# ATUALIZAR ALUNO
@router.put("/students/{student_id}")
def update_student(
    student_id: int,
    data: StudentCreate,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_admin_user)
):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    # Verifica se o email já está sendo usado por outro aluno
    existing = db.query(Student).filter(
        Student.email == data.email,
        Student.id != student_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Email já em uso")

    student.name = data.name
    student.email = data.email

    db.commit()
    db.refresh(student)

    return student

# DELETAR ALUNO
@router.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_admin_user)
):
    db_student = db.query(Student).filter(Student.id == student_id).first()

    if not db_student:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    db.delete(db_student)
    db.commit()

    return {"message": "Student deleted"}
