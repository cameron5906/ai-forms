from pydantic import BaseModel
from enum import Enum

class GroupingType(Enum):
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"

class ElementGroup(BaseModel):
    order: int
    element_ids: list[str]
    grouping_type: GroupingType
