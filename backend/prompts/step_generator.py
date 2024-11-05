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
    
    @tool("Generate a step", force_if=lambda self: self.step is None)
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
            print(f"Executing code:\n{code}")
            
            # Using `exec` to run the code within a limited local environment
            local_env = {}
            exec(code, {}, local_env)
            result = local_env.get("result", "Code executed successfully but did not return a 'result' variable.")
            
            # Return the result or success message
            print(f"Code executed successfully, result: {result}")
            
            return str(result)
        except Exception as e:
            # Capture and format the exception details
            print(f"Error executing code: {traceback.format_exc()}")
            return f"Error executing code: {traceback.format_exc()}"
    
    async def generate_step(self, session_type: SessionType, history: list[BaseChatMessage], description: str, inputs: Optional[dict] = None) -> tuple[Step, list[BaseChatMessage]]:
        from ai.openai_models import GPT4o
        model = GPT4o()
        
        print(f"Executing step generation")
        
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
- You can use the 'execute_code' tool to perform calculations or other computations
- ALL elements must be contained within a group
- Groups MUST specify an 'order', which is its position in the form. Elements should be positioned in a logical order.

Code Execution Guidelines:
- You can execute basic Python code using the 'execute_code' tool.
- Your code must use base Python, you cannot use any external libraries or packages.
- Your code must return a result variable at the top level of the code so it can be captured.

Element Usage Guidelines:

Text Elements:
- Use for introductions, instructions, and informational content
- You must specify a label, which acts as a header for the element
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
  * Sex (Male, Female, Other)
  * Predefined selections (e.g., departments, roles)
- Avoid for: yes/no questions or binary choices

Boolean Elements:
- Use for yes/no questions
- Cannot be placed in a horizontal group
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

Remember:
- Group related fields together to improve user experience
- Use appropriate validation through required fields
- Keep steps focused and not overwhelming
- Ensure all elements align with the form's purpose
""".strip())
        
        if session_type == SessionType.VOICE or session_type == SessionType.TEXT:
            self.add_user_message("""
This form will be taken over a voice call, so you need to describe each field in the step in the step description so the user knows what to say.
If the user does not specify an answer, you will re-prompt them, slightly tweaking the question to encourage a response.

Given this is fundamentally different from the regular step submission process, you will keep each step to a maximum of one input or set of related inputs. Ensure the step description is appropriate with this in mind.

You WILL NOT use text elements in voice mode, instead you will roll up all details into the step description.

Additionally, you will not use words like 'type' or 'input', rather you will use 'say' or 'describe' since this is a voice call.
""".strip())
        
        self.add_user_message(description)
        
        self.add_history(history)
        
        if inputs:
            self.add_user_message(json.dumps(inputs))
        else:
            self.add_user_message("No inputs provided")
            
        returned_messages = await model.get_responses(self)
        
        return self.step, returned_messages
