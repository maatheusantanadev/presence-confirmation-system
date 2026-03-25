from pydantic import BaseModel, EmailStr, Field, validator


# STUDENTS
class StudentCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)

    email: EmailStr

    @validator("name")
    def nome_nao_vazio(cls, v):
        if not v.strip():
            raise ValueError("Nome não pode ser vazio")
        return v


# USERS
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=20)

    password: str

    role: str

    @validator("password")
    def senha_forte(cls, v):
        if len(v) < 8:
            raise ValueError("Senha deve ter pelo menos 8 caracteres")

        if not any(char.isdigit() for char in v):
            raise ValueError("Senha deve conter pelo menos um número")

        return v
