import os
from config import *

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": f"Reads the content of a file relative to the working directory, truncated at {MAX_CHARS} characters",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file to read, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:

    try:
        working_dir_abs_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs_path, file_path))

        common_path = os.path.commonpath([working_dir_abs_path, target_path])
        is_valid_target_directory = common_path == working_dir_abs_path

        if not is_valid_target_directory:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_path) as file:
            content = file.read(MAX_CHARS)

            if file.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

            return content

    except Exception as e:
        return f'Error: {e}'