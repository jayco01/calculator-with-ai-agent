import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content to a file relative to the working directory, creating or overwriting it",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file to write, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs_path, file_path))

        common_path = os.path.commonpath([working_dir_abs_path, target_path])
        is_valid_target_directory = common_path == working_dir_abs_path

        if not is_valid_target_directory:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        with open(target_path, "w") as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"