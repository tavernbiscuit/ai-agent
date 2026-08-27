import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a specified Python file, with optional arguments, and returns the output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Python script to be executed.",
                },
                "args": {
                    "type": "array",
                    "description": "Optional args to be passed to the Python script.",
                        "items": {
                            "type": "string",
                        },
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
        working_dir_abs = os.path.abspath(working_directory)
        full_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_file_path = os.path.commonpath([working_dir_abs, full_file_path]) == working_dir_abs



        if not valid_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", full_file_path]

        if args:
            command.extend(args)

        result = subprocess.run(command, capture_output=True, text=True, timeout=30, cwd=working_dir_abs)


        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"

        if result.stderr and result.stdout == None:
            return "No output produced"

        output_string = f"STDOUT: {result.stdout} STDERR: {result.stderr}"

        return output_string

    except Exception as e:
        return f"Error: {e}"
    

    