from pydantic import BaseModel

#Students
class StudentCreate(BaseModel):
    name: str
    email: str

# Users
class UserCreate(BaseModel):
    username: str
    password: str
    role: str
