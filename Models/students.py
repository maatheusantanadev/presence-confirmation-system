from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Database.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    attendances = relationship("Presence", back_populates="student")
