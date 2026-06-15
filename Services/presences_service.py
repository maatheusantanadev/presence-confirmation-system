import unicodedata
import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session
from sqlalchemy import func

from Models.presence import Presence
from Models.students import Student
from Models.groups import Group

# ---- Configuração do código dinâmico ----
CODE_TTL_SECONDS = 60          # quanto tempo cada código vale (e de quanto em quanto renova)
CODE_LENGTH = 6
# Alfabeto sem caracteres ambíguos (sem 0/O, 1/I/L) pra facilitar digitação manual
_ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"


def _normalizar(texto: str) -> str:
    """Tira acento, caixa e espaços extras pra comparação tolerante."""
    if not texto:
        return ""
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return " ".join(texto.lower().split())


def _agora() -> datetime:
    """Sempre em UTC (consistente com o Render)."""
    return datetime.now(timezone.utc)


def gerar_codigo_turma(group_id: int, db: Session) -> dict:
    """Gera (ou renova) o código dinâmico de uma turma."""
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise ValueError("Turma não encontrada.")

    codigo = "".join(secrets.choice(_ALPHABET) for _ in range(CODE_LENGTH))
    group.current_code = codigo
    group.code_expires_at = _agora() + timedelta(seconds=CODE_TTL_SECONDS)

    db.commit()
    db.refresh(group)

    return {
        "code": codigo,
        "expires_at": group.code_expires_at.isoformat(),
        "ttl_seconds": CODE_TTL_SECONDS,
    }


def validar_codigo_turma(group_id: int, codigo: str, db: Session) -> Group:
    """Valida o código informado contra o código atual da turma."""
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise ValueError("Turma não encontrada.")

    if not group.current_code or not group.code_expires_at:
        raise ValueError("Nenhum código ativo para esta turma. Peça ao professor para gerar.")

    # Supabase pode devolver datetime "naive"; assumimos UTC nesse caso
    expira = group.code_expires_at
    if expira.tzinfo is None:
        expira = expira.replace(tzinfo=timezone.utc)

    if _agora() > expira:
        raise ValueError("Código expirado. Peça um novo ao professor.")

    if (codigo or "").strip().upper() != group.current_code.upper():
        raise ValueError("Código inválido.")

    return group


def create_attendance_by_name(full_name: str, group_id: int, db: Session):
    """
    Busca o aluno pelo nome (tolerante a acento/caixa/espaço)
    e registra a presença em uma turma específica.

    Retorna (presence, created) — created=True quando inseriu agora,
    False quando já existia presença hoje (não duplica).
    """
    alvo = _normalizar(full_name)

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
        return existente, False

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
        return new_attendance, True
    except Exception:
        db.rollback()
        raise