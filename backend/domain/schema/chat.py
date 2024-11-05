from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID
import uuid
from sqlmodel import Field, Relationship, SQLModel

class SessionType(Enum):
    WEB = "web"
    TEXT = "text"
    VOICE = "voice"

class ChatSessionBase(SQLModel):
    form_id: uuid.UUID = Field(nullable=False)
    created_at_utc: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class ChatSession(ChatSessionBase, table=True):
    __tablename__ = "chat_sessions"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    session_type: SessionType = Field(nullable=False)
    phone_number: Optional[str] = Field(nullable=True)
    current_step_json: Optional[str] = Field(nullable=True)
    messages: list["ChatMessage"] = Relationship(back_populates="chat_session")

class ChatMessageBase(SQLModel):
    session_id: uuid.UUID = Field(nullable=False, foreign_key="chat_sessions.id")
    is_user: bool = Field(nullable=False)
    content: Optional[str] = Field()
    created_at_utc: datetime = Field(nullable=False, default_factory=datetime.utcnow)

class ChatMessage(ChatMessageBase, table=True):
    __tablename__ = "chat_messages"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    chat_session: "ChatSession" = Relationship(back_populates="messages")
    tool_calls: list["ChatToolCall"] = Relationship(back_populates="chat_message")

class ChatToolCallBase(SQLModel):
    tool_name: str = Field(nullable=False)
    json_arguments: str = Field(nullable=False)

class ChatToolCall(ChatToolCallBase, table=True):
    __tablename__ = "chat_tool_calls"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    message_id: uuid.UUID = Field(default=None, foreign_key="chat_messages.id")
    tool_call_id: str = Field(nullable=False)
    result: str = Field(nullable=False)
    
    chat_message: "ChatMessage" = Relationship(back_populates="tool_calls")