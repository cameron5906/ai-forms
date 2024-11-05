from typing import List, Optional
from .base_element import BaseElement

class DropdownElement(BaseElement):
    """
    Represents a dropdown menu on the UI.
    """
    options: List[str]
    placeholder: Optional[str] = None
    allow_multiple: bool = False
    values: Optional[List[str]] = None
    
    pass

