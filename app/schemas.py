from datetime import datetime, date
from pydantic import BaseModel, ConfigDict, field_validator

class HabitCreate(BaseModel):
    name: str
    description: str | None = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("name cannot be blank")
        return v.strip()

class HabitUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class HabitResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str | None
    is_active: bool
    created_at: datetime

class CheckinCreate(BaseModel):
    checked_in_on: date | None = None  # defaults to today in the route
    note: str | None = None

class CheckinResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    habit_id: int
    checked_in_on: date
    note: str | None

class StatsResponse(BaseModel):
    habit_id: int
    current_streak: int
    longest_streak: int
    total_checkins: int
    completion_rate_30d: float  # 0.0–100.0
