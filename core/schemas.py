from datetime import date, datetime, timezone
from typing import Optional, Type, TypedDict
from pydantic import BaseModel, EmailStr

class ConstraintErrorHandling(TypedDict):
    constraint: str
    error: Type[Exception]
    message: str

class BaseSchema(BaseModel):
    class Config:
        extra = "forbid"

class UserBase(BaseSchema):
    email: EmailStr
    password: str

class UserRegister(UserBase):
    username: str
    name: str

class UserPwdChange(BaseSchema):
    new_password: str

class UserLogin(UserBase):
    keep_login: bool


class MucleGroup(BaseSchema):
    group_name: str
    user_id: Optional[int]


class UpdateMuscleGroup(BaseSchema):
    group_name: str


class Equipment(BaseSchema):
    group_name: str
    equipment_name: str


class Muscle(BaseSchema):
    muscle_group: str
    muscle_name: str


class Exercise(BaseSchema):
    exercise_name: str
    muscle_id: int
    equipment_id: Optional[int]
    description: Optional[str]


class WorkoutPlan(BaseSchema):
    workout_plan_name: str
    workout_plan_goal: str


class WorkoutSplit(BaseSchema):
    split: str
    workout_plan_id: int


class SplitExercise(BaseSchema):
    split: str
    workout_plan_id: int
    exercise_id: int
    execution_order: int
    sets: int
    reps: str | int
    advanced_technique: Optional[str]
    rest_time: int


class WorkoutReport(BaseSchema):
    report_date: date = datetime.now(timezone.utc).date()
    split: str
    workout_plan_id: int


class SetReport(BaseSchema):
    split: str
    workout_plan_id: int
    exercise_id: int
    execution_order: int
    set_number: int
    workout_report_id: int
    reps: str
    weight: int
    notes: str


class UpdateMuscle(BaseSchema):
    muscle_group: Optional[str] = None
    muscle_name: Optional[str] = None


class UpdateEquipment(BaseSchema):
    group_name: Optional[str] = None
    equipment_name: Optional[str] = None


class UpdateExercise(BaseSchema):
    exercise_name: Optional[str] = None
    muscle_id: Optional[int] = None
    equipment_id: Optional[int] = None
    description: Optional[str] = None


class UpdateWorkoutPlan(BaseSchema):
    workout_plan_name: Optional[str] = None
    workout_plan_goal: Optional[str] = None


class UpdateSplitExercise(BaseSchema):
    split: str
    workout_plan_id: int
    exercise_id: int
    current_execution_order: int  # execution order in database
    execution_order: Optional[int]  # new execution order
    sets: Optional[int] = None
    reps: Optional[str] = None
    advanced_technique: Optional[str] = None
    rest_time: Optional[int] = None


class InactivateSplitExercise(BaseSchema):
    split: str
    workout_plan_id: int
    exercise_id: int
    execution_order: int
