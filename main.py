import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise RuntimeError("OpenRouter API key not set")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")


args = parser.parse_args()

messages = [
    {"role": "user", "content": args.user_prompt},
]

response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
)

prompt_tokens_used = response.usage.prompt_tokens
completion_tokens_used = response.usage.completion_tokens

response_content = response.choices[0].message.content

if response_content is None:
    raise RuntimeError("OpenRouter response content not set")

if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {prompt_tokens_used}")
    print(f"Response tokens: {completion_tokens_used}")

print(response_content)