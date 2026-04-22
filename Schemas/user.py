from pydantic import BaseModel, Field, field_validator
import re

class UserCreate(BaseModel):
    model_config = {
        "str_strip_whitespace": True
    }

    full_name: str = Field(min_length=3, max_length=100)
    cpf: str = Field(description="CPF do professor (apenas números)")
    username: str = Field(min_length=3, max_length=20)
    password: str

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v: str):
        if not v.strip():
            raise ValueError("O nome completo não pode estar vazio")
        return v

    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, v: str):
        cpf_limpo = re.sub(r"\D", "", v)
        if len(cpf_limpo) != 11:
            raise ValueError("O CPF deve conter exatamente 11 dígitos")
        return cpf_limpo

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str):
        return v.lower().strip()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str):
        if len(v) < 6:
            raise ValueError("Senha deve ter pelo menos 6 caracteres")
        if not any(char.isdigit() for char in v):
            raise ValueError("Senha deve conter pelo menos um número")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Senha deve conter pelo menos uma letra maiúscula")
        return v