import json
from collections.abc import Callable

from config import WORKING_DIRECTORY
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_files import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file

available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file,
]

function_map: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "write_file": write_file,
    "run_python_file": run_python_file,
}


def tool_message(tool_call_id: str, content: str) -> dict:
    return {"role": "tool", "tool_call_id": tool_call_id, "content": content}


def call_function(tool_call, verbose: bool = False) -> dict:
    function_name = tool_call.function.name
    function_arguments = json.loads(tool_call.function.arguments or "{}")

    if verbose:
        print(f" - Calling function: {function_name}({function_arguments})")
    else:
        print(f" - Calling function: {function_name}")

    if function_name not in function_map:
        return tool_message(tool_call.id, f"Error: Unknown function: {function_name}")

    # injected last so the model can never choose the working directory
    result = function_map[function_name](
        **{**function_arguments, "working_directory": WORKING_DIRECTORY}
    )

    return tool_message(tool_call.id, result)


def run_tool_calls(tool_calls: list, verbose: bool) -> list[dict]:
    """Run each tool call and return one tool message per call."""
    tool_messages = []

    for tool_call in tool_calls:
        message = call_function(tool_call, verbose)

        if not message["content"]:
            raise Exception("No content provided")

        if verbose:
            print(f"-> {message['content']}")

        tool_messages.append(message)

    return tool_messages
