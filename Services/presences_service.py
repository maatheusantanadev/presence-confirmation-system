import unicodedata
from sqlalchemy.orm import Session
from sqlalchemy import func
from Models.presence import Presence
from Models.students import Student
from datetime import datetime


def _normalizar(texto: str) -> str:
    """Tira acento, caixa e espaços extras pra comparação tolerante."""
    if not texto:
        return ""
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return " ".join(texto.lower().split())


def create_attendance_by_name(full_name: str, group_id: int, db: Session):
    """
    Busca o aluno pelo nome (tolerante a acento/caixa/espaço)
    e registra a presença em uma turma específica.
    """
    alvo = _normalizar(full_name)

    # Compara já normalizado dos dois lados
    student = next(
        (s for s in db.query(Student).all() if _normalizar(s.name) == alvo),
        None
    )

    if not student:
        print(f"ERRO: Aluno '{full_name}' não encontrado no banco.")
        raise ValueError(f"Aluno {full_name} não cadastrado no sistema.")

    # Evita presença duplicada no mesmo dia/turma
    hoje = datetime.now().date()
    existente = db.query(Presence).filter(
        Presence.student_id == student.id,
        Presence.group_id == group_id,
        func.date(Presence.date) == hoje
    ).first()

    if existente:
        print(f"Aviso: {student.name} já tem presença hoje na turma {group_id}.")
        return existente

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
        print(f"✅ Presença confirmada: {student.name} na turma {group_id}")
        return new_attendance
    except Exception as e:
        db.rollback()
        raise e