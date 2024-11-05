from uuid import UUID
from fastapi import HTTPException
from repositories.forms import get_form_by_id, get_form_schema
from repositories.chat import create_chat_session
from prompts.step_generator import StepGenerator
from domain.dto.step import Step
from .chat import save_messages
from domain.schema.chat import SessionType

async def create_session(form_id: UUID, session_type: SessionType) -> tuple[UUID, Step]:
    form = await get_form_by_id(form_id)
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    
    new_session = await create_chat_session(form_id, session_type)
    step_generator = StepGenerator(form)
    
    form_instructions = form.form_information
    
    step, returned_messages = await step_generator.generate_step(session_type=session_type, description=form_instructions, history=[])
    await save_messages(new_session.id, returned_messages)
    
    return new_session.id, step
