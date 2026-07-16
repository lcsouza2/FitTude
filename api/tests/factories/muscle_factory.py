from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from api.src.models import Muscle

class MuscleFactory(SQLAlchemyFactory[Muscle]): ...
