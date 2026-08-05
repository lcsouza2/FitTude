from .schemas_utils import ORMCamelCaseSchema

class MuscleGroupCreateSchema(ORMCamelCaseSchema):
    group_name: str
    user_id: int | None = None

class MuscleGroupUpdateSchema(ORMCamelCaseSchema):
    user_id: int | None = None

class MuscleGroupResponseSchema(ORMCamelCaseSchema):
    group_name: str
    user_id: int | None = None
    deleted: bool
