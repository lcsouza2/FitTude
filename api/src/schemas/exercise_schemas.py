from pydantic import BaseModel

class Exercise(BaseModel):
    exercise_name: str
    description: str


class ExerciseUpdate(BaseModel):
    exercise_name: str | None = None
    muscle_id: int | None = None
    equipment_id: int | None = None
    description: str | None = None