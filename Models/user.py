from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Database.database import Base
from Models.groups import Group

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    cpf = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="professor")

    # Esta linha deve bater com o back_populates do Group
    groups = relationship("Group", back_populates="professor")