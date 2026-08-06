from datetime import date
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, create_tables
from app import crud, stats
from app.models import Habit
from app.schemas import (
    HabitCreate, HabitUpdate, HabitResponse,
    CheckinCreate, CheckinResponse, StatsResponse,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(title="Habit Tracker", lifespan=lifespan)


def _habit_response(habit: Habit, today: date) -> HabitResponse:
    """Serialize a Habit ORM object, populating current_streak from app/stats.py."""
    return HabitResponse(
        id=habit.id,
        name=habit.name,
        description=habit.description,
        is_active=habit.is_active,
        created_at=habit.created_at,
        current_streak=stats.current_streak(
            [c.checked_in_on for c in habit.checkins], today
        ),
    )


# ── Habits ────────────────────────────────────────────────────────────────────

@app.post("/habits", response_model=HabitResponse, status_code=201)
def create_habit(data: HabitCreate, db: Session = Depends(get_db)):
    return _habit_response(crud.create_habit(db, data), date.today())

@app.get("/habits", response_model=list[HabitResponse])
def list_habits(active_only: bool = False, db: Session = Depends(get_db)):
    today = date.today()
    return [_habit_response(h, today) for h in crud.list_habits(db, active_only=active_only)]

@app.get("/habits/{habit_id}", response_model=HabitResponse)
def get_habit(habit_id: int, db: Session = Depends(get_db)):
    habit = crud.get_habit(db, habit_id)
    if not habit:
        raise HTTPException(404, "Habit not found")
    return _habit_response(habit, date.today())

@app.put("/habits/{habit_id}", response_model=HabitResponse)
def update_habit(habit_id: int, data: HabitUpdate, db: Session = Depends(get_db)):
    habit = crud.get_habit(db, habit_id)
    if not habit:
        raise HTTPException(404, "Habit not found")
    return _habit_response(crud.update_habit(db, habit, data), date.today())

@app.post("/habits/{habit_id}/archive", response_model=HabitResponse)
def archive_habit(habit_id: int, db: Session = Depends(get_db)):
    habit = crud.get_habit(db, habit_id)
    if not habit:
        raise HTTPException(404, "Habit not found")
    return _habit_response(crud.archive_habit(db, habit), date.today())

# ── Check-ins ─────────────────────────────────────────────────────────────────

@app.post("/habits/{habit_id}/checkins", response_model=CheckinResponse, status_code=201)
def create_checkin(habit_id: int, data: CheckinCreate = CheckinCreate(), db: Session = Depends(get_db)):
    habit = crud.get_habit(db, habit_id)
    if not habit:
        raise HTTPException(404, "Habit not found")
    checkin = crud.create_checkin(db, habit, data, today=date.today())
    if checkin is None:
        raise HTTPException(409, "Already checked in on this date")
    return checkin

@app.get("/habits/{habit_id}/checkins", response_model=list[CheckinResponse])
def list_checkins(habit_id: int, db: Session = Depends(get_db)):
    if not crud.get_habit(db, habit_id):
        raise HTTPException(404, "Habit not found")
    return crud.list_checkins(db, habit_id)

@app.delete("/habits/{habit_id}/checkins/{checkin_id}", status_code=204)
def delete_checkin(habit_id: int, checkin_id: int, db: Session = Depends(get_db)):
    checkin = crud.get_checkin(db, checkin_id)
    if not checkin or checkin.habit_id != habit_id:
        raise HTTPException(404, "Check-in not found")
    crud.delete_checkin(db, checkin)

# ── Stats ─────────────────────────────────────────────────────────────────────

@app.get("/habits/{habit_id}/stats", response_model=StatsResponse)
def get_stats(habit_id: int, db: Session = Depends(get_db)):
    habit = crud.get_habit(db, habit_id)
    if not habit:
        raise HTTPException(404, "Habit not found")
    dates = [c.checked_in_on for c in habit.checkins]
    today = date.today()
    return StatsResponse(
        habit_id=habit_id,
        current_streak=stats.current_streak(dates, today),
        longest_streak=stats.longest_streak(dates),
        total_checkins=len(dates),
        completion_rate_30d=stats.completion_rate_30d(dates, today),
    )
