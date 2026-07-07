from pydantic import BaseModel

class Muscle(BaseModel):
    group_name: str
    muscle_name: str


class MuscleUpdate(BaseModel):
    muscle_group: str | None = None
    muscle_name: str | None = None