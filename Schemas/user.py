from pydantic import BaseModel, Field, validator

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str
    role: str

    @validator("username")
    def username_lowercase(cls, v):
        v = v.lower()

        if not v.strip():
            raise ValueError("Username não pode estar vazio")

        return v

    @validator("password")
    def senha_forte(cls, v):
        if len(v) < 6:
            raise ValueError("Senha deve ter pelo menos 6 caracteres")

        if not any(char.isdigit() for char in v):
            raise ValueError("Senha deve conter pelo menos um número")

        return v

    @validator("role")
    def role_valido(cls, v):
        if not v or not v.strip():
            raise ValueError("Role não pode estar vazio")

        return v