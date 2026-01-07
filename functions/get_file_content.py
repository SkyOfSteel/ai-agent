import os
from config import CHARACTER_LIMIT
from google import genai
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file in a specified directory relative to the working directory, limited to a certain number of characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)

def get_file_content(working_directory, file_path):
    absolute_path = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(absolute_path, file_path))
    valid_target_file = os.path.commonpath([absolute_path, target_file]) == absolute_path
    if not valid_target_file:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(target_file, "r") as file:
            content = file.read(CHARACTER_LIMIT)
        return content
    except Exception:
        return f'Error: Failed to read file: "{file_path}"'