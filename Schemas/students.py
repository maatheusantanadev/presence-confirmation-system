from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional

class StudentCreate(BaseModel):
    name: str
    email: EmailStr  # Validação automática de formato de email
    registration_number: str
    group_id: Optional[int] = None # Campo opcional para o vínculo direto

    @field_validator("name")
    def nome_nao_vazio(cls, v):
        if not v.strip():
            raise ValueError("Nome não pode ser vazio")
        return v