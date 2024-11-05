import json
import traceback
from typing import Optional
from ai.base_prompt import BasePrompt
from ai.tool_decorator import tool
from domain.dto.step import Step
from ai.base_models import BaseChatMessage
from domain.schema.chat import SessionType

class StepGenerator(BasePrompt):
    step: Optional[Step] = None

    def setup(self) -> None:
        pass
    
    @tool("Generate a step")
    async def provide_step(self, step: Step) -> str:
        self.step = step
        return "Step generated"
    
    @tool("Execute Python code")
    async def execute_code(self, code: str) -> str:
        """
        Execute the provided Python code in a safe environment and return the output.
        
        Parameters:
            code (str): The Python code to execute.

        Returns:
            str: The output or error message from the code execution.
        """
        try:
            # Using `exec` to run the code within a limited local environment
            local_env = {}
            exec(code, {}, local_env)
            result = local_env.get("result", "Code executed successfully but did not return a 'result' variable.")
            
            # Return the result or success message
            return str(result)
        except Exception as e:
            # Capture and format the exception details
            return f"Error executing code: {traceback.format_exc()}"
    
    async def generate_step(self, session_type: SessionType, history: list[BaseChatMessage], description: str, inputs: Optional[dict] = None) -> tuple[Step, list[BaseChatMessage]]:
        from ai.openai_models import GPT4o
        model = GPT4o()
        
        self.set_system_prompt(f"""
You are a form generator that creates one step at a time based on the provided description. Your role is to:

1. Create form elements using the 'provide_step' tool to display them to the user
2. Generate only ONE step at a time - users will submit their answers before receiving the next step
3. Strictly follow the form description when creating elements
4. Group related elements together when appropriate using grid layouts
5. Once your mission is complete, present a final step using the 'provide_step' tool

Guidelines:
- Every form MUST begin with an introduction step using text elements
- Each step should be focused and logical
- Wait for user submission before generating the next step
- EVERY RUN you must provide a new step using the 'provide_step' tool
- Your final step MUST be marked as 'is_final_step' and contain only text elements
- DO NOT reference the next step in any of your steps
- The final step DOES NOT HAVE A SUBMIT BUTTON

Element Usage Guidelines:

Text Elements:
- Use for introductions, instructions, and informational content
- Never mark as required
- Size options: "sm" (details), "md" (normal text), "lg" (headings)

Input Elements:
- Text input: For names, addresses, open-ended responses
- Number input: For age, quantities, numeric values
- Date input: For birthdates, appointments, deadlines
- Multiline: For longer text responses like comments
- Is_sensitive: For passwords or sensitive information

Dropdown Elements:
- Use when there are predefined options (3 or more choices)
- Perfect for: 
  * Countries, states, cities
  * Categories or types
  * Predefined selections (e.g., departments, roles)
- Avoid for: yes/no questions or binary choices

Boolean Elements:
- Use for yes/no questions
- Perfect for:
  * Consent checkboxes
  * Toggle settings
  * Agreement confirmations

Star Rating Elements:
- Use for satisfaction ratings
- Perfect for:
  * Product reviews
  * Service feedback
  * Experience ratings

Element Groups:
- Horizontal groups: Maximum 2 elements (e.g., first name + last name)
- Vertical groups: Related fields that should be visually connected

{'IMPORTANT: This is a voice call, so you must fill in the `voice_friendly` field for each element, this is what will be read out loud to request the information. Text fields can be used to speak to them, which means you can create steps that are just text. Text-only steps are automatically submitted.' if session_type == SessionType.VOICE else ''}
{'IMPORTANT: This is a text chat, so you must fill in the `voice_friendly` field for each element, this is what will be displayed to request the information. Text fields can be used to speak to them, which means you can create steps that are just text. Text-only steps are automatically submitted.' if session_type == SessionType.TEXT else ''}
{'IMPORTANT: Do not fill in the `voice_friendly` field, this is only used for voice calls.' if session_type == SessionType.WEB else ''}

Remember:
- Group related fields together to improve user experience
- Use appropriate validation through required fields
- Keep steps focused and not overwhelming
- Ensure all elements align with the form's purpose
""".strip())
        
        if session_type == SessionType.VOICE:
            self.add_user_message("""
This form will be taken over a voice call, so you should create elements that can be easily transcribed from speech to text.
""".strip())
        
        if session_type == SessionType.TEXT:
            self.add_user_message("""
This form will be taken over a text chat, so you should create elements that can be easily understood from text input.
""".strip())
        
        self.add_user_message(description)
        
        self.add_history(history)
        
        if inputs:
            self.add_user_message(json.dumps(inputs))
        
        returned_messages = await model.get_responses(self)
        
        return self.step, returned_messages
