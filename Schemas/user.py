from pydantic import BaseModel, Field, field_validator
import re


class UserCreate(BaseModel):
    model_config = {
        "str_strip_whitespace": True
    }
    
    username: str = Field(min_length=3, max_length=20)
    password: str
    role: str | None = "admin"

    # ========================================
    # USERNAME
    # ========================================
    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str):
        v = v.lower()

        if not v.strip():
            raise ValueError("Username não pode estar vazio")

        return v

    # ========================================
    # PASSWORD
    # ========================================
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str):

        if len(v) < 6:
            raise ValueError("Senha deve ter pelo menos 6 caracteres")

        if not any(char.isdigit() for char in v):
            raise ValueError("Senha deve conter pelo menos um número")

        if not re.search(r"[A-Z]", v):
            raise ValueError("Senha deve conter letra maiúscula")

        return v

    # ========================================
    # ROLE
    # ========================================
    @field_validator("role")
    @classmethod
    def validate_role(cls, v):
        if v is None:
            return "admin"

        if not isinstance(v, str) or not v.strip():
            raise ValueError("Role não pode estar vazio")

        return v
    