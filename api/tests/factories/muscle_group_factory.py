from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from src.models.muscle_group_models import MuscleGroup

class MuscleGroupFactory(SQLAlchemyFactory[MuscleGroup]): ...
