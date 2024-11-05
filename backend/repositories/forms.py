from sqlalchemy import select
from uuid import UUID
from common.database import get_db
from domain.schema.form import Form, FormValue

async def get_form_by_id(form_id: UUID) -> Form | None:
    async with get_db() as db:  # Get a database session
        query = select(Form).where(Form.id == form_id)
        form = await db.execute(query)
        return form.scalar_one_or_none()

async def create_form(form: Form) -> Form:
    async with get_db() as db:  # Get a database session
        db.add(form)
        await db.commit()
        return form

async def get_forms() -> list[Form]:
    async with get_db() as db:
        forms = await db.execute(select(Form))
        forms = forms.scalars().all()
        return forms
    
async def create_form_value(form_id: UUID, session_id: UUID, field_id: str, value: str) -> FormValue:
    async with get_db() as db:
        form_value = FormValue(form_id=form_id, session_id=session_id, field_id=field_id, value=value)
        db.add(form_value)
        await db.commit()
        return form_value

async def get_form_values(form_id: UUID, session_id: UUID) -> list[FormValue]:
    async with get_db() as db:
        form_values = await db.execute(select(FormValue).where(FormValue.form_id == form_id, FormValue.session_id == session_id))
        form_values = form_values.scalars().all()
        return form_values
    
async def get_form_schema(form_id: UUID) -> list[str]:
    async with get_db() as db:
        form_values_all_unique_keys = await db.execute(select(FormValue.field_id).where(FormValue.form_id == form_id))
        form_values_all_unique_keys = form_values_all_unique_keys.scalars().all()
        return list(set(form_values_all_unique_keys))

async def append_form_instructions(form_id: UUID, instructions: str) -> None:
    async with get_db() as db:
        form = await get_form_by_id(form_id)
        form.form_information += instructions
        await db.commit()
