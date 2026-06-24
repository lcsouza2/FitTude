from pydantic import BaseModel

class SplitExercise(BaseModel):    
    split: str
    workout_plan_id: int
    exercise_id: int
    execution_order: int
    sets: int
    reps: str | int
    advanced_technique: str | None = None
    rest_time: int


class SplitExerciseUpdate(BaseModel):
    split: str
    workout_plan_id: int
    exercise_id: int
    current_execution_order: int  # execution order in database
    execution_order: int  # new execution order
    sets: str | None = None
    reps: str | None = None
    advanced_technique: str | None = None
    rest_time: int | None = None


class InactivateSplitExercise(BaseModel):
    split: str
    workout_plan_id: int
    exercise_id: int
    execution_order: int