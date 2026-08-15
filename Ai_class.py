import json, datetime
from openai import OpenAI
from info import system_prompt
from pathlib import Path
FOLDER_DIR = Path(__file__).resolve().parent

with open(FOLDER_DIR / "config.json", "r") as file:
    config = json.load(file)

local_ip = config["LOCAL_IP"]
first_client = OpenAI(
    base_url=f"http://{local_ip}:11434/v1",
    api_key="ollama" 
)
second_client = OpenAI(
    base_url=f"http://{local_ip}:11434/v1",
    api_key="ollama" 
)
def log_to_console(filepath: str, module_name: str, text: str):
    time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{time}] [{filepath}] [{module_name}] {text}")

def call_the_chat(message):
    if not message:
        return "I don't know"
    
    
    log_to_console((Path(__file__).name), "TEXT AI", "received a message for text ai")
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"<user_query>\n{message}<user_query>\n"}
    ]

    try:
        response = first_client.chat.completions.create(
            model="richardyoung/qwen2.5-7b-instruct-abliterated:latest",
            messages=messages,
            temperature=0.0,
            extra_body={
                "options": {
                    "num_ctx": 16384,
                    "repeat_penalty": 1.2,
                    "stop": ["\n\n\n", "User:", "System:"]
                }
            }
        )
        return response.choices[0].message.content
    except Exception as e:
        log_to_console((Path(__file__).name), "TEXT AI", f"text ai error: {e}")
        return "I don't know"

def call_the_vl(base64_data):
    log_to_console((Path(__file__).name), "VISUAL AI", f"received a message for visual ai")
    try:
        response = second_client.chat.completions.create(
            model="qwen2.5vl:3b",  
            messages=[
                {"role": "system","content": "ZERO TOLERANCE POLICY. Any image showing crypto withdrawals, Suspicious links that don't look like any known legit casinos, fake transaction histories, online casino panels, promo code reward boxes, or celebrity crypto giveaways (like MrBeast/Andrew Tate claiming free money) is a 100% malicious phishing scam. Analyze this image. Answer strictly with format: 'VERDICT: SCAM' or 'VERDICT: SAFE'. Add really concise reasoning as to why (do it in format 'VERDICT: SAFE/SCAM | reasoning') don't forget to add a '|' character"},
                {"role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_data}"
                        }
                    }
                ]
            }],
            temperature=0.0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        log_to_console((Path(__file__).name), "VISUAL AI", f"visual ai error: {e}")
        return "SAFE | couldn't test the image"