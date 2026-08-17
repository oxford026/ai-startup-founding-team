import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6")
MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "3"))
