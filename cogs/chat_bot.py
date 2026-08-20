import json, discord, datetime, aiofiles
from discord.ext import commands
from helper_scripts.Ai_class import call_the_chat
from pathlib import Path
#from testfile import query_knowledge_base
class Chat_bot(commands.Cog):
    def __init__(self, client):
        self.client = client

        FOLDER_DIR = Path().resolve()
        self.FILES = {
            "question_logger": FOLDER_DIR / "storage/QaA.txt",
            "questions": FOLDER_DIR / "storage/QuestionRequests.txt",
            "config": FOLDER_DIR / "storage/config.json"
        }
        print(self.FILES["config"])

        with open(self.FILES["config"], mode="r") as file:
            self.config = json.load(file)

        #decided to play with output a bit, make it more "fun"
    def log_to_console(self, filepath: str, module_name: str, text: str):
        time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{time}] [{filepath}] [{module_name}] {text}")

    @commands.command()
    async def question(self, ctx: commands.Context):
        askinguser = ctx.author.name
                
        try:
            user_question = ctx.message.content.split(None, 1)[1]
        except IndexError:
            await ctx.message.reply("You need to provide a question.")
            return
        
        answer = await call_the_chat(user_question) 
        print(answer)

        await ctx.message.reply(f"{answer}\n-# this is SUPER WIP, so don't expect it answer any questions.")
        async with aiofiles.open(self.FILES["question_logger"], "a", encoding="utf-8") as file:
            await file.write(f"{askinguser}\n{ctx.message.content}\n{answer}\n---------\n")
        self.log_to_console((Path(__file__).name), "question", f"wrote to the {Path(self.FILES['question_logger']).name} file")

    @commands.command()
    async def submit_question(self, ctx: commands.Context):
        reason = ctx.message.content.split(None, 1)[1]
        with open(self.FILES["questions"], "a", encoding="utf-8") as file:
            file.write(f"{reason}\n---------\n")
        self.log_to_console((Path(__file__).name), "submit_question", f"wrote to the {Path(self.FILES['questions']).name} file ")

async def setup(bot):
    await bot.add_cog(Chat_bot(bot))
