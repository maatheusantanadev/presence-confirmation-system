# Models/associations.py
from sqlalchemy import Table, Column, Integer, ForeignKey
from Database.database import Base

group_members = Table(
    "group_members",
    Base.metadata,
    Column("group_id", Integer, ForeignKey("groups.id"), primary_key=True),
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True)
)