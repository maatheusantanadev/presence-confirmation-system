# Models/groups.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Database.database import Base
from Models.associations import group_members # IMPORTAÇÃO AQUI

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    professor_cpf = Column(String, ForeignKey("users.cpf"), nullable=False)

    professor = relationship("User", back_populates="groups")
    students = relationship("Student", secondary=group_members, back_populates="groups")