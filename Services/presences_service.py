from sqlalchemy.orm import Session
from Models.presence import Presence
from Models.students import Student
from datetime import datetime


def create_attendance_by_name(full_name: str, db: Session):
    """
    Busca o aluno pelo nome completo e registra a presença.
    """
    # 1. Busca o aluno pelo nome no seu banco local
    # Usamos .lower() para evitar problemas com maiúsculas/minúsculas
    student = db.query(Student).filter(Student.name.ilike(full_name.strip())).first()

    if not student:
        print(f"ERRO: Aluno '{full_name}' não encontrado no banco local.")
        raise ValueError(f"Aluno {full_name} não cadastrado no sistema.")

    # 2. Cria o registro de presença com o ID real do banco local
    new_attendance = Presence(
        student_id=student.id,
        date=datetime.now(),
        status="presente"
    )

    try:
        db.add(new_attendance)
        db.commit()
        db.refresh(new_attendance)
        print(f"✅ Presença confirmada para: {student.name} (ID Local: {student.id})")
        return new_attendance
    except Exception as e:
        db.rollback()
        raise e