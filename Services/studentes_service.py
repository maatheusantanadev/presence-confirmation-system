from sqlalchemy.orm import Session
from Models.students import Student
from Models.groups import Group


def create_student(name: str, email: str, registration_number: str, db: Session, group_id: int = None):
    """
    REGRA DE NEGÓCIO:
    - validar nome, email e matrícula
    - evitar duplicidade por email e matrícula
    - vincular a uma turma opcionalmente
    """

    # 1. Validação de campos vazios
    if not name or not name.strip():
        raise ValueError("Nome inválido")

    if not email or "@" not in email:
        raise ValueError("Email inválido")

    if not registration_number or not registration_number.strip():
        raise ValueError("Matrícula é obrigatória")

    # 2. Evitar duplicidade de Email
    if db.query(Student).filter_by(email=email).first():
        raise ValueError("Este email já está cadastrado")

    # 3. Evitar duplicidade de Matrícula (Crítico para o funcionamento das turmas)
    if db.query(Student).filter_by(registration_number=registration_number).first():
        raise ValueError("Este número de matrícula já existe")

    # 4. Criação do Objeto Student com todos os campos obrigatórios
    new_student = Student(
        name=name.strip(),
        email=email.strip().lower(),
        registration_number=registration_number.strip()
    )

    try:
        db.add(new_student)
        db.flush()  # Gera o ID do aluno sem fechar a transação

        # 5. Vínculo opcional com Turma (Caso venha do formulário de turma)
        if group_id:
            group = db.query(Group).filter(Group.id == group_id).first()
            if group:
                group.students.append(new_student)
            else:
                raise ValueError("Turma destino não encontrada")

        db.commit()
        db.refresh(new_student)
        return new_student

    except Exception as e:
        db.rollback()
        raise e