from functions.get_files_info import *
from functions.get_file_content import *
from functions.write_file import *
from functions.run_python_files import *

available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file,
]

def call_function(tool_call, verbose: bool = False) -> dict:
    function_name = tool_call.function.name
    function_arguments = tool_call.function.arguments
    tool_call_id = tool_call.id

