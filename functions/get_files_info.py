import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    working_dir_abs = os.path.abspath(working_directory)

    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    try:
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        
        dir_contents = os.listdir(target_dir)
        dir_contents_list = []
        for item in dir_contents:
            full_item_path = os.path.normpath(os.path.join(target_dir, item))
            is_dir = False
            if os.path.isdir(full_item_path):
                file_size = os.path.getsize(full_item_path)
                is_dir = True
                dir_contents_list.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")

            else:
                file_size = os.path.getsize(full_item_path)
                dir_contents_list.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")

        return '\n'.join(dir_contents_list)

    except Exception as e:
        return f"Error: {e}"