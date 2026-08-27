import os
from config import MAX_CHARS # type: ignore

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Retrieve content from file and return it as a variable.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to the file that will be opened by the function. (Created from working directory)."
                },
            },
            "required": ["file_path"],
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    full_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_file_path = os.path.commonpath([working_dir_abs, full_file_path]) == working_dir_abs

    try:
        if not valid_file_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(full_file_path) as f:
            file_content = f.read(MAX_CHARS)
            if f.read(MAX_CHARS+1):
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

            return file_content
        
    except Exception as e:
            return f"Error: {e}"

