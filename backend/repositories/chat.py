from typing import Optional
from uuid import UUID
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
from domain.dto.step import Step
from common.database import get_db
from domain.schema.chat import ChatSession, ChatMessage, SessionType

async def create_chat_session(form_id: UUID, session_type: SessionType):
    async with get_db() as db:
        chat_session = ChatSession(form_id=form_id, session_type=session_type)
        db.add(chat_session)
        await db.commit()
        return chat_session

async def insert_messages(messages: list[ChatMessage]):
    async with get_db() as db:
        db.add_all(messages)
        await db.commit()
from sqlalchemy.orm import joinedload

async def get_messages(session_id: UUID) -> list[ChatMessage]:
    async with get_db() as db:
        messages = await db.execute(
            select(ChatMessage)
            .options(joinedload(ChatMessage.tool_calls))
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at_utc)
        )
        return messages.scalars().unique().all()

async def update_current_step(session_id: UUID, current_step: Step):
    async with get_db() as db:
        await db.execute(
            update(ChatSession).where(ChatSession.id == session_id).values(current_step_json=current_step.model_dump_json())
        )
        await db.commit()

async def get_current_step(session_id: UUID) -> Optional[Step]:
    """
    Retrieve the current step for a given chat session.

    Parameters:
        session_id (UUID): The unique identifier for the chat session.

    Returns:
        Step: The current step associated with the chat session.
    """
    async with get_db() as db:
        chat_session = await db.execute(
            select(ChatSession).where(ChatSession.id == session_id)
        )
        session = chat_session.scalar_one_or_none()

        if session is None or session.current_step_json is None:
            return None
        
        return Step.model_validate_json(session.current_step_json)
