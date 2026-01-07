import os
from google import genai
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    absolute_path = os.path.abspath(working_directory)
    target_directory = os.path.normpath(os.path.join(absolute_path, directory))
    valid_target_directory = os.path.commonpath([absolute_path, target_directory]) == absolute_path
    if not valid_target_directory:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_directory):
        return f'Error: "{directory}" is not a directory'
    result = []
    for item in os.listdir(target_directory):
        full_path = os.path.join(target_directory, item)
        try:
            if os.path.isfile(full_path):
                item_string = f"- {str(item)}: file_size={os.path.getsize(full_path)} bytes, is_dir=False"
            elif os.path.isdir(full_path):
                item_string = f"- {str(item)}: file_size={os.path.getsize(full_path)} bytes, is_dir=True"
            else:
                continue
            result.append(item_string)
        except Exception:
            return f"Error: Failed to get info for item: {item}"
    final_result = "\n".join(result)
    return f"{final_result}"