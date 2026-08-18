import json, datetime
from openai import OpenAI
from helper_scripts.info import text_prompt, scam_prompt
from pathlib import Path

FOLDER_DIR = Path().resolve()
with open(FOLDER_DIR / "storage/config.json", "r") as file:
    config = json.load(file)

local_ip = config["LOCAL_IP"]

client = OpenAI(
    base_url=f"http://{local_ip}:11434/v1",
    api_key="ollama" 
)

def log_to_console(filepath: str, module_name: str, text: str):
    time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{time}] [{filepath}] [{module_name}] {text}")

# Call the text ai
async def call_the_chat(message):
    log_to_console((Path(__file__).name), "TEXT AI", "received a message for text ai")

    messages = [
        {"role": "system", "content": text_prompt},
        {"role": "user", "content": f"<user_query>\n{message}<user_query>\n"}
    ]
    
    try:
        response = client.chat.completions.create(
            model="richardyoung/qwen2.5-7b-instruct-abliterated:latest",
            messages=messages,
        )
        return response.choices[0].message.content
    except Exception as e:
        log_to_console((Path(__file__).name), "TEXT AI", f"text ai error: {e}")
        return "I don't know"
    
# Call the vosial ai
async def call_the_vl(base64_data):
    log_to_console((Path(__file__).name), "VISUAL AI", f"received a message for visual ai")

    messages = [
        {"role": "system", "content": scam_prompt},
        {"role": "user", "content": [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_data}"}}]}
    ]

    try:
        response = client.chat.completions.create(
            model="qwen2.5vl:3b",  
            messages=messages
        )
        print(response.choices[0].message.content.strip())        
        return response.choices[0].message.content.strip()
    except Exception as e:
        log_to_console((Path(__file__).name), "VISUAL AI", f"visual ai error: {e}")
        return "SAFE | couldn't test the image"