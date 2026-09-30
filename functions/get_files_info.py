import os
from os.path import commonpath


def get_files_info(working_directory: str, directory: str = ".") -> str:
    working_dir_abs_path = os.path.abspath(working_directory)
    target_directory = os.path.normpath(os.path.join(working_dir_abs_path, directory))

    common_path = os.path.commonpath([working_dir_abs_path, target_directory])
    is_valid_target_directory = common_path == working_dir_abs_path

    try:
        if not is_valid_target_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_directory):
            return f'Error: "{directory}" is not a directory'

        return f'Success: "{directory}" is within the working directory'
    except Exception as e:
        return f'Error: {e}'