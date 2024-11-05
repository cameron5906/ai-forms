from domain.schema.form import Form
from repositories.forms import create_form

async def create_new_form(title: str, description: str) -> Form:
    form = Form(
        title=title,
        form_information=description
    )
    return await create_form(form)