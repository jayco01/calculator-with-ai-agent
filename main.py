import argparse

from call_function import run_tool_calls
from llm import create_client, generate_content
from prompt import system_prompt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    client = create_client()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    response = generate_content(client, messages)
    ai_message = response.choices[0].message
    tool_messages = run_tool_calls(ai_message.tool_calls or [], args.verbose)


if __name__ == "__main__":
    main()
