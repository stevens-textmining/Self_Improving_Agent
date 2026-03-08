import os
import sys
from tabnanny import verbose

from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_files_info import schema_get_files_info
import functions
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from call_function import call_function

def main():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=api_key)
    verbose_flag = False

    system_prompt = (

        """
        1:
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
    
        - List files and directories
        - Read the content of a file
        - Write to a file(create or update)
        - Run a Python file with optional arguments
    
        All paths you provide should be relative to the working directory. 
        
        You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """
    )

    if len(sys.argv) < 2:
        print("We need a prompt!!")
        sys.exit(1)
    elif len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True


    userPrompt = sys.argv[1]

    message = [
        types.Content(role="user", parts=[types.Part(text=userPrompt)])
    ]

##TOOL for The LLM to use!!!------------------------------------------------------------------------------------
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file

        ]
    )

    config = types.GenerateContentConfig(
        tools = [available_functions], system_instruction=system_prompt
    )

    max_iters = 20

    ## 开启Agent Loop！！，最多iteration次 给他个20次
    for i in range(0, max_iters):



        response = client.models.generate_content(
            model='gemini-2.5-flash',
            #这里的contents要用message
            contents=message,
            config=config,
        )
        if verbose_flag:
            print("user prompt",{userPrompt})
            print("prompt tokens: ", {response.usage_metadata.prompt_token_count})
            print("response tokens: ", {response.usage_metadata.candidates_token_count})


        if response is None or response.usage_metadata is None:
            print("response not worked")
            return



        if response.candidates:
            for candidate in response.candidates:
                if candidate is None or candidate.content is None:
                    continue
                message.append(candidate.content)


        if response.function_calls:
            for function_call_part in response.function_calls:

                result = call_function(function_call_part, verbose_flag)
                message.append(result)

        else:
            #final agent text message

            print(response.text)
            break















if __name__ == "__main__":
    main()