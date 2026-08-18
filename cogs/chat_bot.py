import json, discord, io, base64
from discord.ext import commands
from Ai_class import call_the_chat, call_the_vl
from pathlib import Path
from PIL import Image

class Chat_bot(commands.Cog):
    def __init__(self, client):
        self.client = client

        FOLDER_DIR = Path().resolve()
        self.FILES = {
            "question_logger": FOLDER_DIR / "QaA.txt",
            "questions": FOLDER_DIR / "QuestionRequests.txt",
            "config": FOLDER_DIR / "config.json"
        }

        with open(self.FILES["config"], mode="r") as file:
            self.config = json.load(file)

async def setup(bot):
    await bot.add_cog(Chat_bot(bot))
