from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from Database.database import Base
from datetime import datetime

class Presence(Base):
    __tablename__ = "presences"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="presente")

    student = relationship("Student", back_populates="attendances")