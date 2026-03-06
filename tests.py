from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
def main():
    working_dir = "calculator"
    #print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    #print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))


    #print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
    #Return: Error: "/tmp/temp.txt" is not in the working directory
    #print(write_file("calculator", "dirNotExsistBefore/temp.txt", "this should not be allowed"))

    # print(run_python_file("calculator", "main.py"))
    # print(run_python_file("calculator", "tests.py"))
    # print(run_python_file("calculator", "../main.py"))
    # print(run_python_file("calculator", "Nonexsistent.py"))

    # print(run_python_file("calculator", "main.py",["3 + 6"]))



main()