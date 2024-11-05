import os

def get_openai_key() -> str:
    return os.getenv("OPENAI_API_KEY")