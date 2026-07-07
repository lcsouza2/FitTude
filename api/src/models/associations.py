from sqlalchemy import String, Table, Column, Integer, ForeignKey
from api.src.models.base_models import BaseOrmModel
from api.src.utils.constraints import DatabaseConstraints

assoc_exercise_muscle = Table(
    "exercise_muscle",
    BaseOrmModel.metadata,
    Column("exercise_id", Integer, ForeignKey("exercise.exercise_id", name=DatabaseConstraints.ExerciseMuscle.FK_EXERCISE), primary_key=True),
    Column("muscle_id", Integer, ForeignKey("muscle.muscle_id", name=DatabaseConstraints.ExerciseMuscle.FK_MUSCLE), primary_key=True),
)

assoc_exercise_equipment = Table(
    "exercise_equipment",
    BaseOrmModel.metadata,
    Column("exercise_id", Integer, ForeignKey("exercise.exercise_id", name=DatabaseConstraints.ExerciseEquipment.FK_EXERCISE), primary_key=True),
    Column("equipment_id", Integer, ForeignKey("equipment.equipment_id", name=DatabaseConstraints.ExerciseEquipment.FK_EQUIPMENT), primary_key=True),
)

assoc_split_exercise = Table(
    "split_exercise",
    BaseOrmModel.metadata,
    Column("split", Integer, ForeignKey("workout_split.split", name=DatabaseConstraints.SplitExercise.FK_WORKOUT_SPLIT), primary_key=True),
    Column("exercise_id", Integer, ForeignKey("exercise.exercise_id", name=DatabaseConstraints.SplitExercise.FK_EXERCISE), primary_key=True),
    Column("execution_order", Integer, primary_key=True),
    Column("sets", Integer),
    Column("reps", String, default="Failure"),
    Column("rest_time", Integer),
    Column("advanced_technique", String, nullable=True),
    Column("deleted", Integer, default=False),
)
