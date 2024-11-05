from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, HTTPException, Response, Request
from pydantic import BaseModel
from domain.dto.step import Step
from domain.schema import FormResponse
from services.form_creation import create_new_form
from services.form_progression import execute_with_form_input, execute_with_text_input
from services.sessions import create_session
from repositories.forms import get_form_by_id, get_forms, get_most_recent_form
from repositories.chat import update_current_step, get_session_from_phone_number
from domain.schema.chat import SessionType
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.twiml.messaging_response import MessagingResponse
from prompts import StepToTextTranslator

router = APIRouter()

class FormCreate(BaseModel):
    title: str
    description: str
    
class FormValues(BaseModel):
    values: dict

@router.post("/forms/", response_model=FormResponse)
async def create_form(form: FormCreate):
    return await create_new_form(form.title, form.description)

@router.get("/forms/{form_id}", response_model=Step)
async def get_form(form_id: UUID):
    form = await get_form_by_id(form_id)
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    
    return Step(
        title=form.title,
        description=form.description,
        elements=form.elements,
        groups=form.groups
    )

@router.get("/forms/", response_model=List[FormResponse])
async def get_all_forms():
    return await get_forms()

@router.post("/forms/{form_id}/session")
async def create_new_session(form_id: UUID):
    session_id, step = await create_session(form_id, SessionType.WEB)
    await update_current_step(session_id, step)
    return {
        "session_id": session_id,
        "step": step
    }
    
@router.post("/forms/{form_id}/session/text")
async def create_new_text_session(form_id: UUID, phone_number: Optional[str] = None):
    session_id, step = await create_session(form_id, SessionType.TEXT, phone_number)
    await update_current_step(session_id, step)
    return {
        "session_id": session_id,
        "step": step
    }

@router.post("/forms/{form_id}/session/{session_id}")
async def continue_session(form_id: UUID, session_id: UUID, values: FormValues):
    return await execute_with_form_input(form_id, session_id, values.values)

@router.post("/forms/{form_id}/session/{session_id}/transcribe")
async def continue_session_with_transcript(form_id: UUID, session_id: UUID, transcript: str):
    return await execute_with_text_input(form_id, session_id, transcript)

@router.post("/forms/call")
async def handle_incoming_call(request: Request):
    """
    Handle incoming Twilio voice calls by initiating a text-based session
    Returns TwiML response to gather user input
    """
    most_recent_form = await get_most_recent_form()
    if not most_recent_form:
        raise HTTPException(status_code=404, detail="No forms found")
    
    form_id = most_recent_form.id
    
    # Reuse existing text session creation
    session_response = await create_new_text_session(form_id)
    session_id = session_response["session_id"]
    step: Step = session_response["step"]
    
    response = VoiceResponse()
    gather = Gather(
        input='speech',
        action=f'/api/forms/{form_id}/session/{session_id}/voice',
        method='POST',
        language='en-US',
        timeout=15,
        speech_timeout='auto'
    )
    gather.say(await StepToTextTranslator().get_step_text(step))
    
    response.append(gather)
    
    return Response(
        content=str(response),
        media_type="application/xml"
    )

@router.post("/forms/{form_id}/session/{session_id}/voice")
async def handle_voice_input(form_id: UUID, session_id: UUID, request: Request):
    """
    Handle voice input by passing it through the existing text-based flow
    Returns TwiML response for the next step
    """
    form_data = await request.form()
    transcript = form_data.get('SpeechResult', '')
    
    # Reuse existing text input processing
    result = await continue_session_with_transcript(
        form_id=form_id,
        session_id=session_id,
        transcript=transcript
    )
    
    response = VoiceResponse()
    
    response.say(await StepToTextTranslator().get_step_text(result))
    
    if result.is_final_step:
        response.hangup()
    else:
        gather = Gather(
            input='speech',
            action=f'/api/forms/{form_id}/session/{session_id}/voice',
            method='POST',
            language='en-US',
            timeout=15,  # Adjust the timeout to determine how long to wait for speech input
            speech_timeout='auto'  # Automatically end the gathering when speech stops
        )
        
        response.append(gather)
    
    return Response(
        content=str(response),
        media_type="application/xml"
    )

@router.post("/forms/sms")
async def handle_incoming_sms(request: Request):
    """
    Handle incoming Twilio SMS messages by initiating a text-based session
    Returns TwiML response with the form question
    """
    most_recent_form = await get_most_recent_form()
    if not most_recent_form:
        raise HTTPException(status_code=404, detail="No forms found")
    
    form_id = most_recent_form.id
    
    form_data = await request.form()
    sms_body = form_data.get('Body', '')
    phone_number = form_data.get('From', '')
    
    existing_session = await get_session_from_phone_number(phone_number)
    is_new_session = False
    
    if existing_session:
        session_id = existing_session.id
    else:
        session_response = await create_new_text_session(form_id, phone_number=phone_number)
        session_id = session_response["session_id"]
        is_new_session = True
        
    step = await continue_session_with_transcript(form_id, session_id, sms_body if not is_new_session else "Let's begin")
    
    response = MessagingResponse()
    response_text = await StepToTextTranslator().get_step_text(step)
    
    response.message(body=response_text)
    
    return Response(
        content=str(response),
        media_type="application/xml"
    )