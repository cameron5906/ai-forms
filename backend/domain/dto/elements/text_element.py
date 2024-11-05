from typing import Literal
from .base_element import BaseElement

class TextElement(BaseElement):
    """
    Represents a paragraph of text on the UI.
    """
    
    text: str
    size: Literal["sm", "md", "lg"]
    
    pass