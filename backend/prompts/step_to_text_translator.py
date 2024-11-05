from ai.base_prompt import BasePrompt
from domain.dto.step import Step

class StepToTextTranslator(BasePrompt):
    async def get_step_text(self, step: Step):
        from ai.openai_models import GPT4o
        model = GPT4o()
        
        print(f"Executing step to text generation", step)
        
        self.set_system_prompt("""
Your task is to translate JSON that outlines a step in a form into natural language that could be understood by the user
over the phone. Your goal is to ask them for information if there any inputs in the form, or to explain text elements to them by reading them aloud.
This should sound natural and conversational.

You will respond only with the message that will be sent to the user.
""".strip())
        
        self.add_user_message(step.model_dump_json())
        
        responses = await model.get_responses(self)
        
        return responses[0].message