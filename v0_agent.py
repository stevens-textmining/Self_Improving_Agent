from asyncio import timeout

from anthropic import Anthropic
import subprocess,sys,os
from dotenv import load_dotenv

load_dotenv()
API =os.getenv("api_key_kimi")

client = Anthropic(api_key=API, base_url="https://api.moonshot.cn/anthropic")

TOOL = [
    {
        "name":"bash",
        "description":"""Execute shell command. Common patterns:
        
        - Read: cat/head/tail, grep/find/rg/ls, wc -l
        - Write: echo 'content' > file, sed -i 's/old/new/g' file
        - Subagent: python v0_agent.py 'task description' (spawns isolated agent, returns summary)
        
        """,
        "input_schema":{
            "type":"object",
            "properties":{"command": {"type": "string"}},
            "required": ["command"]

        }

    }


]

SYSTEM = f"""CLI agent at {os.getcwd()}. ALWAYS use the bash tool to execute commands. 
            NEVER output commands as text - call the bash tool instead. Spawn subagent for complex tasks.
            IF the user use Chinese, reponse with Chinese"""

def chat(prompt, history = []):
    history.append({"role": "user","content":prompt})
    while True:
        response = client.messages.create(
            max_tokens=8000,
            model="kimi-k2-turbo-preview",
            messages=history,
            system=SYSTEM,
            tools=TOOL,
        )
        history.append({"role":"assistant","content":response.content})
        if response.stop_reason != "tool_use":
            return "".join(b.text for b in response.content if hasattr(b,"text"))
        results = []
        for b in response.content:
            if b.type == "tool_use":
                out = subprocess.run(b.input["command"],shell=True, capture_output=True, text = True,timeout = 300)
                results.append({"type": "tool_result", "tool_use_id": b.id, "content": out.stdout + out.stderr})
        history.append({"role":"user","content":results})

if __name__ =="__main__":
    if len(sys.argv) >1:
        print(chat(sys.argv[1]))
    else:
        h=[]
        while (q:=input(">> ")) not in ("q","","stop"):
            print(chat(q,h))
        print("Bye")




