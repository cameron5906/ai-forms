from typing import Union
from pydantic import BaseModel
from .elements import InputElement, TextElement, DropdownElement, ElementGroup, BooleanElement, StarRatingElement

class Step(BaseModel):
    title: str
    description: str
    elements: list[Union[InputElement, TextElement, DropdownElement, BooleanElement, StarRatingElement]]
    groups: list[ElementGroup]
    required_element_ids: list[str]
    is_final_step: bool
