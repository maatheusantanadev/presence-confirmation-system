# Models/students.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Database.database import Base
from Models.associations import group_members # IMPORTAÇÃO AQUI
from Models.groups import Group

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    registration_number = Column(String, unique=True, nullable=False)

    groups = relationship("Group", secondary=group_members, back_populates="students")
    attendances = relationship("Presence", back_populates="student")