import os

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletion

from call_function import available_functions
from config import MODEL


def create_client() -> OpenAI:
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("OpenRouter API key not set")

    return OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)


def generate_content(client: OpenAI, messages: list) -> ChatCompletion:
    return client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=available_functions,
    )
