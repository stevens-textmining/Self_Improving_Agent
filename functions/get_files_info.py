import os.path


def get_files_info(working_directory, directory = None):
    abs_working_dir = os.path.abspath(working_directory)
    if directory is None:
        directory = "."

    abs_directory = os.path.abspath(directory)
    if not abs_directory.startswith(abs_working_dir):
        return f'Error: "{directory}" is not a direcotry'


    contents = os.listdir(abs_directory)
    for content in contents:
        is_dir = os.path.isdir(os.path.join(abs_directory, content))