from pydantic import BaseModel
from typing import List, Optional

# Esquema para exibir dados simplificados do aluno dentro da turma
class StudentInGroup(BaseModel):
    id: int
    name: str
    email: str
    registration_number: str

    class Config:
        from_attributes = True

class GroupBase(BaseModel):
    name: str
    professor_cpf: str

class GroupCreate(GroupBase):
    # Usado no POST: Recebe as matrículas para vincular os alunos
    student_registration_numbers: List[str]

class GroupResponse(BaseModel):
    id: int
    name: str
    professor_cpf: str
    # O segredo está aqui: o SQLAlchemy vai preencher isso automaticamente
    # através do relacionamento 'students' que definimos no Model
    students: List[StudentInGroup] = []

    class Config:
        from_attributes = True