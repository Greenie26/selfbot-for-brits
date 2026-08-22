# i fucking HATE these llms, have to rewrite them every single fucking time
import json, datetime
from ollama import AsyncClient
from helper_scripts.info import scam_prompt, get_prompt
from pathlib import Path

FOLDER_DIR = Path().resolve()
with open(FOLDER_DIR / "storage/config.json", "r") as file:
    config = json.load(file)

local_ip = config["LOCAL_IP"]

client = AsyncClient(host=f"http://{local_ip}:11434")

def log_to_console(filepath: str, module_name: str, text: str):
    time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{time}] [{filepath}] [{module_name}] {text}")

# call the text ai
async def call_the_chat(message):
    log_to_console((Path(__file__).name), "TEXT AI", "received a message for text ai")
    text_prompt = get_prompt(message)

    messages = [
        {"role": "system", "content": text_prompt},
        {"role": "user", "content": f"<user_query>\n{message}\n</user_query>"}
    ]

    try:
        response = await client.chat(
            model="richardyoung/qwen2.5-7b-instruct-abliterated:latest",
            messages=messages
        )

        return response["message"]["content"]
    except Exception as e:
        log_to_console((Path(__file__).name), "TEXT AI", f"text ai error: {e}")
        return "I don't know"
    
# call the vosial ai
async def call_the_vl(base64_data):
    log_to_console((Path(__file__).name), "VISUAL AI", f"received a message for visual ai")

    messages=[
        {"role": "system", "content": scam_prompt},
        {"role": "user", "content": "Analyze this image and determine if it's a scam or safe", "images": [base64_data]}
    ]

    try:
        response = await client.chat(
            model="qwen2.5vl:7b", # different models tried: 9 (man i hate working with these low parameter vl models.) (7 HOURS OF FUCKING DEBUGING, FUCK THESE VL LLMS) Oh god, it's fucking working, IT'S FUCKING WORKING!
            messages=messages,
            options={"num_ctx": 2048 * 2}
        )
        print(response)
        print(response["message"]["content"])

        return response["message"]["content"].strip()
    except Exception as e:
        log_to_console((Path(__file__).name), "VISUAL AI", f"visual ai error: {e}")
        return "SAFE | couldn't test the image"