# schemas/presence.py

from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

VALID_STATUS = ["presente", "ausente", "justificado"]


class PresenceCreate(BaseModel):
    student_id: int
    date: Optional[datetime] = None
    status: str = "presente"

    @field_validator("status")
    def validate_status(cls, v):
        v = v.lower().strip()
        if v not in VALID_STATUS:
            raise ValueError("Status inválido")
        return v

    @field_validator("date")
    def validate_date(cls, v):
        if v and v > datetime.utcnow():
            raise ValueError("Data não pode ser futura")
        return v


class PresenceResponse(BaseModel):
    id: int
    student_id: int
    date: datetime
    status: str

    class Config:
        from_attributes = True