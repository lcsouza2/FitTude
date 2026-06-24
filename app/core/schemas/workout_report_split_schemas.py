from pydantic import BaseModel
from datetime import date, datetime, timezone

class WorkoutReport(BaseModel):
    report_date: date = datetime.now(timezone.utc).date()
    split: str
    workout_plan_id: int


class WorkoutSplit(BaseModel):
    split: str
    workout_plan_id: int
    

class SetReport(BaseModel):
    split: str
    workout_plan_id: int
    exercise_id: int
    execution_order: int
    set_number: int
    workout_report_id: int
    reps: str
    weight: int
    notes: str