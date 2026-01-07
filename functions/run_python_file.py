import os
import subprocess
from google import genai
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in a specified directory relative to the working directory and returns its output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of arguments to pass to the Python file",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    absolute_path = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(absolute_path, file_path))
    valid_target_file = os.path.commonpath([absolute_path, target_file]) == absolute_path
    if not valid_target_file:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not target_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    command = ["python", target_file]
    if args:
        command.extend(args)
    try:
        subprocess_result = subprocess.run(command, capture_output=True, text=True, cwd=absolute_path, timeout=30)
        if subprocess_result.returncode != 0:
            return f'Process exited with code {subprocess_result.returncode}'
        if subprocess_result.stderr == None or subprocess_result.stdout == None:
            return 'Error: No output produced'
        return f"STDOUT: {subprocess_result.stdout}\nSTDERR: {subprocess_result.stderr}"
    except Exception:
        return f"Error: executing Python file: {file_path}"
    