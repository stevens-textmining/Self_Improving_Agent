import os
from google.genai import types


def write_file(working_directory:str, file_path:str, content:str):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        #如果这个directory 根本就不在working directory里，那么肯定就是错了，返回不是一个directory
        return f'Error: "{abs_file_path}" is not in the working directory'

    parent_dir = os.path.dirname(abs_file_path)
    #这里检查，file上面的这个directory 是否存在？？如果存在了 我们再去查询，他底下的file是否存在
    if not os.path.isdir(parent_dir):
        try:
            os.makedirs(parent_dir)
        except Exception as e:
            return f"could not create parent dirs: {parent_dir} = {e}"


        #如果给的这个file_path 根本就不是一个文件，我们就创造一个文件在 parent_dir 下面！！
    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to {file_path} (lenth: {len(content)} characters)'
    except Exception as e:
        return f"Failed to write to file: {file_path}, {e}"




schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites an exsisting file,or writes to a new file if it doesnt exsist (and create required parent dirs safely) ",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents to write to the file as a string"



            )
        },
    ),
)