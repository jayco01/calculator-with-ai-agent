import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a Python file relative to the working directory with optional command-line arguments and returns its stdout and stderr",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the Python file to run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional command-line arguments to pass to the Python file",
                },
            },
            "required": ["file_path"],
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs_path, file_path))

        common_path = os.path.commonpath([working_dir_abs_path, target_path])
        is_valid_target_directory = common_path == working_dir_abs_path

        if not is_valid_target_directory:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_path]

        if args:
            command.extend(args)

        completed_process = subprocess.run(command, cwd=working_dir_abs_path, capture_output=True, text=True, timeout=30)

        output_str = ""

        if completed_process.returncode != 0:
            output_str += f"Process exited with code {completed_process.returncode}. "

        if not completed_process.stdout and not completed_process.stderr:
            output_str += "No output produced. "
        else:
            output_str += f"STDOUT: {completed_process.stdout}\n STDERR: {completed_process.stderr}"

        return output_str
    except Exception as e:
        return f"Error: executing Python file: {e}"