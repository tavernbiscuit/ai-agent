import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content taken as string, to a specified file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file that content will be written to.",
                },
                "content": {
                    "type": "string",
                    "description": "Content that function will write to the file.",
                },
            },
            "required": ["file_path, content"],
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    full_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_file_path = os.path.commonpath([working_dir_abs, full_file_path]) == working_dir_abs

    try:
        if not valid_file_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(full_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        root_directory_path = os.path.dirname(full_file_path)
        os.makedirs(root_directory_path, exist_ok=True)

        with open(full_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"