import json, discord, io, base64, datetime, ServerPinging
from discord.ext import commands
from Ai_class import call_the_chat, call_the_vl
from pathlib import Path
from PIL import Image

class Server_status(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.FOLDER_DIR = Path().resolve()
        self.FILES = {
            "config": self.FOLDER_DIR / "storage/config.json"
        }
        with open(self.FILES["config"], mode='r') as file:
            self.config = json.load(file)
        self.ping_messages = {}

        self.GUILD_ID = self.config["TARGET_GUILD_ID"]
        self.BOT_IDS = self.config["BOT_IDS"]

#decided to play with output a bit, make it more "fun"
    def log_to_console(filepath: str, module_name: str, text: str):
        time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{time}] [{filepath}] [{module_name}] {text}")

    async def get_bots(self):
        GUILD = await self.client.fetch_guild(self.GUILD_ID)
        members = await GUILD.query_members(
                user_ids=[
                    int(self.BOT_IDS["USbotID"]),
                    int(self.BOT_IDS["EUbotID"]),
                    int(self.BOT_IDS["AUbotID"])
                    ],
                presences=True,
                subscribe=True
            )
        return members
    # ----------------
    def format_status(self, status_string: str, min_players:int):
        if "Offline" in status_string:
            return status_string

        player = int(status_string.split()[0])
        if player < min_players:
            return f"{player} players online | playercount abnormally low"
        return status_string
    

    #@commands.cooldown(1, 15, commands.BucketType.channel)
    @commands.command()
    async def status(self, ctx: commands.Context):

        #if ctx.channel.id not in ALLOWED_CHANNELS:
        #   return
        
        # load bots so they won't equal to None when you search for them
        self.log_to_console((Path(__file__).name), "status", "loading specific bots into memory.")

        members = await self.get_bots()
        
        self.log_to_console((Path(__file__).name), "status", "bots loaded.")

        USBOT = next((member for member in members if member.id == int(self.BOT_IDS["USbotID"])), None)
        EUBOT = next((member for member in members if member.id == int(self.BOT_IDS["EUbotID"])), None)
        AUBOT = next((member for member in members if member.id == int(self.BOT_IDS["AUbotID"])), None)

        UsStatus = self.format_status(USBOT.activity.name, 50) 
        EuStatus = self.format_status(EUBOT.activity.name, 50)
        AuStatus = self.format_status(AUBOT.activity.name, 10)

        USWorldsDelay =  self.format_delay(ServerPinging.get_us_delay(), 150)
        EUWorldsDelay =  self.format_delay(ServerPinging.get_eu_delay(), 250)
        AUWorldsDelay =  self.format_delay(ServerPinging.get_au_delay(), 320)

        self.log_to_console((Path(__file__).name), "status", "Proccessed everything correctly")

        sent_msg = await ctx.message.reply(
            f"US status - {UsStatus} {USWorldsDelay}\n"
            f"EU status - {EuStatus} {EUWorldsDelay}\n"
            f"AU status - {AuStatus} {AUWorldsDelay}\n"
            f"-# Delays are for client that is located at Southeastern region of USA",
            mention_author=True
        )   
        self.log_to_console((Path(__file__).name), "status", "sent a message correctly")


async def setup(bot):
    await bot.add_cog(Server_status(bot))