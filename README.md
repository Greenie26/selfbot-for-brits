# selfbot-for-brits
Decided to make a small bot that gives me ability to write small utils like scam detection or chatbot

---

## How to install Ollama
* **Linux**: Run `curl -fsSL https://ollama.com/install.sh | sh` in your terminal.
* **Windows**: Download and run the installer from the official [Ollama website](https://ollama.com).

---

To set it up, you need to run

`pip install -r requirements.txt`

--- 

And you need to set up 2 models for ollama

`ollama run richardyoung/qwen2.5-7b-instruct-abliterated:latest`

`ollama run qwen2.5vl:3b`

---
## To set up ollama on linux:
Open ollama config 

`sudo systemctl edit ollama.service`

Add a line at the top
```
[Service]

Environment="OLLAMA_HOST=0.0.0.0:11434"

```

Close and then do

```
sudo systemctl daemon-reload
sudo systemctl restart ollama
```
After that (if you are running it on the other local machine)
```
sudo ufw allow 11434/tcp
```
otherwise you can just leave it be

---
## To set up ollama on windows:
Run
```
[System.Environment]::SetEnvironmentVariable("OLLAMA_HOST", "0.0.0.0:11434", "User")
Restart-Service -Name "OllamaService"
```
and then run this (if you are running it on the other local machine)
```
New-NetFirewallRule -DisplayName "Ollama" -Direction Inbound -Protocol TCP -LocalPort 11434 -Action Allow
```


# Find your local ip and put it into config
for linux you can use
```
hostname -I
```
and for windows
```
ipconfig
```