from uuid import UUID
from repositories.forms import get_form_by_id
from repositories.chat import get_current_step, update_current_step
from .chat import get_history, save_messages
from prompts.step_generator import StepGenerator
from prompts.text_to_inputs_translator import TextToInputsTranslator
from domain.schema.chat import SessionType
from repositories.forms import create_form_value, get_form_values, append_form_instructions

async def execute_with_form_input(form_id: UUID, session_id: UUID, inputs: dict):
    form = await get_form_by_id(form_id)
    history = await get_history(session_id)
    
    for field_id, value in inputs.items():
        await create_form_value(form_id=form_id, session_id=session_id, field_id=field_id, value=value)
    
    step, returned_messages = await StepGenerator().generate_step(SessionType.WEB, history, form.form_information, inputs)
    await update_current_step(session_id, step)
    await save_messages(session_id, returned_messages)
    
    print("Step", step)
    
    if step.is_final_step:
        await handle_completed_form(form_id, session_id)
    
    return step

async def execute_with_text_input(form_id: UUID, session_id: UUID, transcript: str):
    current_step = await get_current_step(session_id)
    
    if current_step is None:
        raise ValueError("No current step found")
    
    values = await TextToInputsTranslator().get_inputs_from_text(transcript, current_step)
    
    print("Values", values)
    
    return await execute_with_form_input(form_id, session_id, values)

async def handle_completed_form(form_id: UUID, session_id: UUID):
    form = await get_form_by_id(form_id)
    history = await get_history(session_id)
    
    form_values = await get_form_values(form_id, session_id)
    
    values_dict = {
        value.field_id: value.value for value in form_values
    }
    
    fields_str = "\n".join([f"- {field}" for field in values_dict.keys()])
    
    await append_form_instructions(form_id, f"\n\nThe form MUST ONLY have the following fields:\n{fields_str}")
    
    print(values_dict)