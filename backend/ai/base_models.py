from enum import Enum
from typing import Any, List, Optional
from pydantic import BaseModel

class BaseTool:
    name: str
    description: str
    schema: dict
    result: Optional[Any] = None
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.schema = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
    def use_schema(self, schema: dict) -> None:
        self.schema = schema
        
    def process(arguments: dict):
        raise NotImplementedError("Method not implemented")
        
class BaseToolCall:
    id: str
    name: str
    arguments: str
    
    def __init__(self, id: str, name: str, arguments: str):
        self.id = id
        self.name = name
        self.arguments = arguments
        
class BaseToolCallWithResult(BaseToolCall):
    result: str
    
    def __init__(
        self, 
        id: str, 
        name: str, 
        arguments: str, 
        result: str
    ):
        super().__init__(
            id, 
            name, 
            arguments
        )
        
        self.result = result

class ChatRole(Enum):
    USER = 1
    AGENT = 2
    TOOL = 3

class BaseChatMessage:
    role: ChatRole
    png_images: List[bytes]
    message: Optional[str]
    tool_calls: List[BaseToolCallWithResult] = []
    
    def __init__(
        self, 
        role: ChatRole, 
        message: Optional[str], 
        png_images: List[bytes] = [],
        tool_calls: List[BaseToolCallWithResult] = []
    ):
        self.role = role
        self.message = message
        self.png_images = png_images
        self.tool_calls = tool_calls
        
class BaseChatResponse(BaseChatMessage):
    tool_calls: List[BaseToolCallWithResult]
    
    def __init__(self, message: str, tool_calls: List[BaseToolCallWithResult]):
        super().__init__(ChatRole.AGENT, message)
        self.tool_calls = tool_calls
        
class Tool(BaseModel):
    name: str
    is_public: bool
    data: Optional[str] = None

class CompletionChunk(BaseModel):
    message_id: str
    received_text: Optional[str] = None
    text: Optional[str] = None
    audio: Optional[str] = None
    tools: Optional[list[Tool]] = None