## AI Form Prototype
This codebase serves as an example implementation of creating and using conditional forms powered by generative AI.

### How it works
1. Define a form with natural language
2. Submit the form instructions, saving them in the database, returning the form id
3. Begin a form
4. Submit step
5. LLM generates JSON describing elements to render with id, label, and other element-specific properties
6. Repeat 3-5 until all information is gathered
7. LLM generates conclusion screen
8. All inputs entered into the form are saved 
