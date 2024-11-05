from typing import Optional
from .base_element import BaseElement, InputType

class InputElement(BaseElement):
    """
    Represents an input field on the UI for values that can be translated to a string.
    """
    
    input_type: InputType
    multiline: bool = False
    placeholder: Optional[str] = None
    value: Optional[str] = None
    is_sensitive: bool = False
    
    pass
