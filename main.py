import os
import sys
from tabnanny import verbose

from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=api_key)
    verbose_flag = False

    if len(sys.argv) < 2:
        print("We need a prompt!!")
        sys.exit(1)
    elif len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True

    else:
        userPrompt = sys.argv[1]

    message = [
        types.Content(role="user", parts=[types.Part(text=userPrompt)])


    ]

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=userPrompt,
    )
    print(response.text)

    if response is None or response.usage_metadata is None:
        print("response not worked")
        return


    if verbose_flag:
        print("user prompt",{userPrompt})
        print("prompt tokens: ", {response.usage_metadata.prompt_token_count})
        print("response tokens: ", {response.usage_metadata.candidates_token_count})


if __name__ == "__main__":
    main()
