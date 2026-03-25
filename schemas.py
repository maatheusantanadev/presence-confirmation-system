from pydantic import BaseModel, EmailStr, Field, validator

# STUDENTS
class StudentCreate(BaseModel):
    # Nome do aluno deve ter entre 3 e 50 caracteres
    name: str = Field(min_length=3, max_length=50)

    # Email do aluno o EmailStr já valida automaticamente o formato
    email: EmailStr

    # Validação para garantir que o nome não seja só espaços
    @validator("name")
    def nome_nao_vazio(cls, v):
        if not v.strip():
            raise ValueError("Nome não pode ser vazio")
        return v

# USERS
class UserCreate(BaseModel):
    # Nome de usuário (login) deve ter entre 3 e 20 caracteres
    username: str = Field(min_length=3, max_length=20)

    # Senha do usuário
    password: str

    # Papel do usuário (ex: admin, professor, etc.)
    role: str

    # Validação de senha
    # - mínimo de 8 caracteres
    # - deve conter pelo menos um número
    @validator("password")
    def senha_forte(cls, v):
        if len(v) < 8:
            raise ValueError("Senha deve ter pelo menos 8 caracteres")

        if not any(char.isdigit() for char in v):
            raise ValueError("Senha deve conter pelo menos um número")

        return v
    