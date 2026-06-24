from pydantic import BaseModel

class WorkoutPlan(BaseModel):
    workout_plan_name: str
    workout_plan_goal: str


class WorkoutPlanUpdate(BaseModel):
    workout_plan_name: str | None = None
    workout_plan_goal: str | None = None