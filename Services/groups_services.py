from sqlalchemy.orm import Session
from Models.groups import Group
from Models.students import Student
from Models.user import User
from typing import List

def create_group(name: str, prof_cpf: str, student_registrations: List[str], db: Session):
    # 1. Validação: Verifica se o professor existe pelo CPF
    professor = db.query(User).filter(User.cpf == prof_cpf).first()
    if not professor:
        raise ValueError(f"Professor com CPF {prof_cpf} não encontrado.")

    # 2. Busca alunos pelas matrículas enviadas
    # Usamos o campo registration_number que definimos no model Student
    students = db.query(Student).filter(Student.registration_number.in_(student_registrations)).all()

    # Verifica se todos os alunos enviados foram encontrados
    if len(students) != len(student_registrations):
        encontrados = [s.registration_number for s in students]
        faltantes = list(set(student_registrations) - set(encontrados))
        raise ValueError(f"As seguintes matrículas são inválidas: {', '.join(faltantes)}")

    # 3. Cria a instância da turma (Group)
    # O SQLAlchemy gerencia a tabela group_members automaticamente ao atribuirmos a lista students
    new_group = Group(
        name=name,
        professor_cpf=prof_cpf,
        students=students
    )

    try:
        db.add(new_group)
        db.commit()
        db.refresh(new_group)
        return new_group
    except Exception as e:
        db.rollback()
        raise Exception(f"Erro ao salvar turma no banco de dados: {str(e)}")

def list_all_groups(db: Session):
    """Retorna todas as turmas com os relacionamentos carregados"""
    return db.query(Group).all()

def get_group_by_id(group_id: int, db: Session):
    """Retorna uma turma específica ou None"""
    return db.query(Group).filter(Group.id == group_id).first()