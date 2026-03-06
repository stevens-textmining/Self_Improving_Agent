import os
from config import MAX_CHARS
from google.genai import types
def get_file_content(working_directory:str, file_path:str):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        # 如果这个directory 根本就不在working directory里，那么肯定就是错了，返回不是一个directory
        return f'Error: "{abs_file_path}" is not in the working directory'

    if not os.path.isfile(abs_file_path):
        return f"Error: {file_path} is not a file"

    file_content_string = ""
    try:

        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)

            if len(file_content_string) >= MAX_CHARS:
                file_content_string += (
                    f'[...File "{file_path}" truncated at 10000 characters]'

                )
        return file_content_string
    except Exception as e:
        return f"Exception reading file: {e}"





schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="gets the content of the given file as a stiring, constrained to working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file_path to the files ,from working directory (default is the working directory itself)",
            ),
        },
    ),
)

