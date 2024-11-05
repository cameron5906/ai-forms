from typing import Optional
from ai.base_prompt import BasePrompt
from ai.tool_decorator import tool
from domain.dto.step import Step

class TextToInputsTranslator(BasePrompt):
    values: Optional[dict] = {}
    
    @tool("Provide the values for the form", force_if=lambda self: True)
    async def provide_inputs(self, values: dict) -> dict:
        self.values = values
        return "Inputs provided"
    
    async def get_inputs_from_text(self, transcript: str, step: Step) -> dict:
        from ai.openai_models import GPT4o
        model = GPT4o()
        
        self.set_system_prompt("""
You will match a provided transcript of a user speaking with the inputs of a form.
Your job is to provide an object with keys being the ids of the elements in the form and values being the derived value from the transcript.
You are allowed to correct minor errors in the transcript, but do not alter the meaning of the transcript.

Do not provide any other information than the values, or an empty object if none of the values match.
""".strip())
        
        form_fields_str = "\n".join([
            f"- {field.label} ({field.element_type}) ID: {field.id}" for field in step.elements   
        ])
        
        self.add_user_message(f"""
Form fields:
{form_fields_str}

Transcript:
{transcript}
        """)
        
        await model.get_responses(self)
        
        return self.values

