from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from src.models import Muscle

class MuscleFactory(SQLAlchemyFactory[Muscle]): ...
