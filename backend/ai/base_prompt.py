from typing import Dict, List, Optional, Type, TypeVar
from .base_models import BaseChatMessage, BaseTool, ChatRole, BaseToolCallWithResult
import ai

T = TypeVar('T', bound='BaseTool')

class BasePrompt:
    system_prompt: str
    messages: List[BaseChatMessage]
    tools: List[str]  # Now we store tool names instead of BaseTool instances
    tool_types: Dict[str, Type[BaseTool]]
    tool_result_types: Dict[str, Type]
    tool_instances: Dict[str, List[BaseTool]]
     
    def __init__(self, system_prompt: Optional[str] = None, tools: List[str] = None) -> None:
        self.messages = []
        self.system_prompt = system_prompt
        self.tools = tools or []
        self.tool_types = {}
        self.tool_result_types = {}
        self.tool_instances = {}
        self.forced_tools = []
        
        self.setup()
    
    def setup(self) -> None:
        pass
    
    async def think(self, model: 'ai.base_gpt.BaseGPT', user_input: str):
        self.add_user_message(user_input)
        responses = await model.get_responses(self)
        for response in responses:
            if response.message:
                self.add_agent_message(response.message)
    
    def set_system_prompt(self, system_prompt: str) -> None:
        self.system_prompt = system_prompt
        
    def add_user_message(self, message: str, png_images: List[bytes] = []) -> None:
        self.messages.append(BaseChatMessage(role=ChatRole.USER, message=message, png_images=png_images))
        
    def add_agent_message(self, message: str, tool_calls: Optional[List[BaseToolCallWithResult]] = None) -> None:
        self.messages.append(BaseChatMessage(role=ChatRole.AGENT, message=message, tool_calls=tool_calls or []))

    def add_history(self, history: List[BaseChatMessage]) -> None:
        for message in history:
            if message.role == ChatRole.USER:
                self.add_user_message(message.message)
            elif message.role == ChatRole.AGENT:
                self.add_agent_message(
                    message=message.message,
                    tool_calls=message.tool_calls
                )
