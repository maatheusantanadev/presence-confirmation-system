from sqlalchemy.orm import Session
from sqlalchemy import func # Importação necessária para comparar apenas a DATA
from Models.presence import Presence
from Models.students import Student
from datetime import datetime

# ADICIONAMOS group_id como parâmetro
def create_attendance_by_name(full_name: str, group_id: int, db: Session):
    """
    Busca o aluno pelo nome completo e registra a presença em uma turma específica.
    """
    # 1. Busca o aluno pelo nome
    student = db.query(Student).filter(Student.name.ilike(full_name.strip())).first()

    if not student:
        print(f"ERRO: Aluno '{full_name}' não encontrado no banco local.")
        raise ValueError(f"Aluno {full_name} não cadastrado no sistema.")

    # 2. Verifica se já existe presença hoje NESTA turma específica
    hoje = datetime.now().date()
    existente = db.query(Presence).filter(
        Presence.student_id == student.id,
        Presence.group_id == group_id, # Agora a variável existe!
        func.date(Presence.date) == hoje
    ).first()

    if existente:
        print(f"Aviso: {student.name} já possui presença hoje na turma {group_id}.")
        return existente

    # 3. Cria a nova presença vinculada à turma
    new_attendance = Presence(
        student_id=student.id,
        group_id=group_id,
        date=datetime.now(),
        status="presente"
    )

    try:
        db.add(new_attendance)
        db.commit()
        db.refresh(new_attendance)
        print(f"✅ Presença confirmada para: {student.name} na turma {group_id}")
        return new_attendance
    except Exception as e:
        db.rollback()
        raise e