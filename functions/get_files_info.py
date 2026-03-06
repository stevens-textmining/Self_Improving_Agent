import os.path
from google.genai import types

def get_files_info(working_directory, directory = '.'):
    '''


    :param working_directory: 这是root directory
    :param directory:  这时候calculator里的directory

    LLM必须在我们指定的 working_directory 里面去工作，比如 只能在 calculator 这个文件里去工作
    '''

    abs_working_dir = os.path.abspath(working_directory)
    abs_directory = os.path.abspath(os.path.join(working_directory, directory))

    if not abs_directory.startswith(abs_working_dir):
        # 如果这个directory 根本就不在working directory里，那么肯定就是错了，返回不是一个directory
        return f'Error: "{directory}" is not in the working direcotry'

    final_response = ""
    contents = os.listdir(abs_directory)
    for content in contents:
        ##判断这个abs_directory 里哪个是文件
        content_path = os.path.join(abs_directory,content)
        is_dir = os.path.isdir(content_path)
        ## file size
        size = os.path.getsize(content_path)

        final_response += f"- {content}: file_size={size} bytes, is_dir={is_dir}\n"

    return final_response

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