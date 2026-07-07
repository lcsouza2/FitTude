class DatabaseConstraints:
    """
    Essa classe mapeia as constaints do banco de dados para que possam ser reutilizadas em diferentes partes do código.
    """

    class User:
        UNIQUE = "uq_user"

    class Muscle:
        UNIQUE = "uq_muscle"
        FK_USER = "fk_muscle_user"
        FK_MUSCLE_GROUP = "fk_muscle_muscle_group"

    class MuscleGroup:
        UNIQUE = "uq_muscle_group"
        FK_USER = "fk_muscle_group_user"

    class Equipment:
        UNIQUE = "uq_equipment"
        FK_USER = "fk_equipment_user"
        FK_MUSCLE_GROUP = "fk_equipment_muscle_group"
        IDX_EQUIPMENT_NAME = "idx_equipment_name"

    class Exercise:
        UNIQUE = "uq_exercise"
        FK_USER = "fk_exercise_user"

    class ExerciseMuscle:
        FK_EXERCISE = "fk_exercise_muscle_exercise"
        FK_MUSCLE = "fk_exercise_muscle_muscle"

    class ExerciseEquipment:
        FK_EXERCISE = "fk_exercise_equipment_exercise"
        FK_EQUIPMENT = "fk_exercise_equipment_equipment"

    class WorkoutPlan:
        UNIQUE = "uq_workout_plan"
        FK_USER = "fk_workout_plan_user"

    class WorkoutSplit:
        FK_WORKOUT_PLAN = "fk_workout_split_workout_plan"

    class SplitExercise:
        FK_WORKOUT_SPLIT = "fk_split_exercise_workout_split"
        FK_EXERCISE = "fk_split_exercise_exercise"

    class WorkoutReport:
        FK_WORKOUT_PLAN = "fk_workout_report_workout_plan"
        FK_WORKOUT_SPLIT = "fk_workout_report_workout_split"

    class SetReport:
        FK_WORKOUT_REPORT = "fk_set_report_workout_report"
        FK_EXERCISE = "fk_set_report_exercise"
        FK_SPLIT = "fk_set_report_split"
        FK_WORKOUT_PLAN = "fk_set_report_workout_plan"