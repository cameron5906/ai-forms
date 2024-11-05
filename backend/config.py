import os
import dotenv

dotenv.load_dotenv()

def get_openai_key() -> str:
    return os.getenv("OPENAI_API_KEY")