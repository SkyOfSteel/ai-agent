# BookBot

An experimental AI Agent based on Google's gemini-2.5-flash. Designed to read and write files in the provided work directory and subdirectories, run Python scripts and suggest code improvements.

# Usage

**`uv run main.py <user_prompt> [--verbose]`**

Replace <user_prompt> with an actual prompt. The program is designed to run in a [uv](https://docs.astral.sh/uv/) environment pinned to Python 3.13.

*--verbose* - lists the original prompt, the number of tokens in the prompt and the tokens used in the AI Agent's response.

The output includes the function calls used by the AI to perform the operation. Available functions:

*get_files_info* - lists files in the working directory.

*get_file_content* - reads the content of a file.

*write_file* - writes the supplied prompt into the file.

*run_python_file* - executes a Python script.

# Example

Command "uv run main.py "Please list the files starting with M in the current directory" --verbose" will produce the following result:

```
User prompt: Please list the files starting with M in the current directory
Prompt tokens: 439
Response tokens: 12
[FunctionCall(id=None, args={}, name='get_files_info')]
Calling function: get_files_info({})
User prompt: Please list the files starting with M in the current directory
Prompt tokens: 586
Response tokens: 22
There is only one file, `main.py`, that starts with 'M' in the current directory.
```