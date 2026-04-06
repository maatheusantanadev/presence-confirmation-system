from pydantic import BaseModel, EmailStr, Field, validator

class StudentCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)

    email: EmailStr

    @validator("name")
    def nome_nao_vazio(cls, v):
        if not v.strip():
            raise ValueError("Nome não pode ser vazio")
        return v

