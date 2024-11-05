from uuid import UUID
from ai.base_models import BaseChatMessage, ChatRole, BaseToolCallWithResult
from domain.schema.chat import ChatMessage, ChatToolCall
from repositories.chat import insert_messages, get_messages

async def save_messages(session_id: UUID, messages: list[BaseChatMessage]):
    chat_messages = [
        ChatMessage(
            session_id=session_id,
            is_user=message.role == ChatRole.USER,
            content=message.message,
            tool_calls=[
                ChatToolCall(
                    tool_call_id=tool_call.id,
                    tool_name=tool_call.name,
                    json_arguments=tool_call.arguments,
                    result=tool_call.result
                )
                for tool_call in message.tool_calls
            ]
        )
        for message in messages
    ]
    
    await insert_messages(chat_messages)

async def get_history(session_id: UUID) -> list[BaseChatMessage]:
    messages = await get_messages(session_id)
    return [
        BaseChatMessage(
            role=ChatRole.USER if message.is_user else ChatRole.AGENT,
            message=message.content,
            tool_calls=[
                BaseToolCallWithResult(
                    id=tool_call.tool_call_id,
                    name=tool_call.tool_name,
                    arguments=tool_call.json_arguments,
                    result=tool_call.result
                )
                for tool_call in message.tool_calls
            ]
        )
        for message in messages
    ]