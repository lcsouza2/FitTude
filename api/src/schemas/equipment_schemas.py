from pydantic import BaseModel

class Equipment(BaseModel):
    group_name: str
    equipment_name: str


class EquipmentUpdate(BaseModel):
    group_name: str | None = None
    equipment_name: str | None = None