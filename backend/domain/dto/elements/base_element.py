from enum import Enum
from typing import Optional

from pydantic import BaseModel

class ElementType(Enum):
    TEXT = "text"
    INPUT = "input"
    DROPDOWN = "dropdown"
    BOOLEAN = "boolean"
    STAR_RATING = "star_rating"
    
class InputType(Enum):
    TEXT = "text"
    NUMBER = "number"
    DATE = "date"
    BOOLEAN = "boolean"

class BaseElement(BaseModel):
    """
    Base element class for all UI elements.
    """
    
    element_type: ElementType
    id: str
    label: str
    