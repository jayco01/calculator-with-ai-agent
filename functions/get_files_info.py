import os
from os.path import commonpath


def get_files_info(working_directory: str, directory: str = ".") -> str:
    working_dir_abs_path = os.path.abspath(working_directory)
    target_directory = os.path.normpath(os.path.join(working_dir_abs_path, directory))

    common_path = os.path.commonpath([working_dir_abs_path, target_directory])
    is_valid_target_directory = common_path == working_dir_abs_path

    directory_name = os.path.basename(target_directory) if target_directory != "" else "current"
    content = f"Result for {directory_name} directory:\n"

    try:
        if not is_valid_target_directory:
            content += f'  Error: Cannot list "{directory}" as it is outside the permitted working directory\n'
            return content

        if not os.path.isdir(target_directory):
            content += f'  Error: "{directory}" is not a directory\n'
            return content

        for file in os.listdir(target_directory):
            file_name = file
            file_size = os.path.getsize(os.path.join(target_directory, file_name))
            is_directory = os.path.isdir(os.path.join(target_directory, file_name))

            content += f" - {file_name}: file_size={file_size} bytes, is_dir={is_directory}\n"

        return content
    except Exception as e:
        return f'Error: {e}'