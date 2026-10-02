import os

from dotenv import load_dotenv
from openai import BadRequestError, OpenAI
from openai.types.chat import ChatCompletion

from call_function import available_functions
from config import MAX_TOOL_RETRIES, MODEL


def create_client() -> OpenAI:
    load_dotenv()
    # api_key = os.getenv("OPENROUTER_API_KEY")
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        # raise RuntimeError("OpenRouter API key not set")
        raise RuntimeError("GROQ API key not set")

    # return OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key) # openrouter rate limit reached, so switching to groq
    return OpenAI(base_url="https://api.groq.com/openai/v1", api_key=api_key)


def generate_content(client: OpenAI, messages: list) -> ChatCompletion:
    request_messages = messages

    for attempt in range(MAX_TOOL_RETRIES):
        try:
            return client.chat.completions.create(
                model=MODEL,
                messages=request_messages,
                tools=available_functions,
            )
        except BadRequestError as e:
            # the provider rejected a malformed tool call: retry, telling the model what was wrong
            if e.code != "tool_use_failed" or attempt == MAX_TOOL_RETRIES - 1:
                raise
            request_messages = messages + [
                {
                    "role": "user",
                    "content": f"Your last tool call was rejected: {e.body['message']} "
                    "Retry using exactly the argument names from the function definitions.",
                }
            ]
