from sqlalchemy import Column, Integer, String
from database import Base

#Students
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)