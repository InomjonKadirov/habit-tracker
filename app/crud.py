from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import Habit, Checkin
from app.schemas import HabitCreate, HabitUpdate, CheckinCreate

def create_habit(db: Session, data: HabitCreate) -> Habit:
    habit = Habit(name=data.name, description=data.description)
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit

def list_habits(db: Session, active_only: bool = False) -> list[Habit]:
    q = db.query(Habit)
    if active_only:
        q = q.filter(Habit.is_active == True)
    return q.order_by(Habit.created_at.asc()).all()

def get_habit(db: Session, habit_id: int) -> Habit | None:
    return db.get(Habit, habit_id)

def update_habit(db: Session, habit: Habit, data: HabitUpdate) -> Habit:
    if data.name is not None:
        habit.name = data.name
    if data.description is not None:
        habit.description = data.description
    db.commit()
    db.refresh(habit)
    return habit

def archive_habit(db: Session, habit: Habit) -> Habit:
    habit.is_active = False
    db.commit()
    db.refresh(habit)
    return habit

def create_checkin(db: Session, habit: Habit, data: CheckinCreate, today: date) -> Checkin | None:
    checkin = Checkin(
        habit_id=habit.id,
        checked_in_on=data.checked_in_on or today,
        note=data.note,
    )
    db.add(checkin)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return None  # duplicate — caller raises 409
    db.refresh(checkin)
    return checkin

def list_checkins(db: Session, habit_id: int) -> list[Checkin]:
    return (
        db.query(Checkin)
        .filter(Checkin.habit_id == habit_id)
        .order_by(Checkin.checked_in_on.desc())
        .all()
    )

def get_checkin(db: Session, checkin_id: int) -> Checkin | None:
    return db.get(Checkin, checkin_id)

def delete_checkin(db: Session, checkin: Checkin) -> None:
    db.delete(checkin)
    db.commit()
