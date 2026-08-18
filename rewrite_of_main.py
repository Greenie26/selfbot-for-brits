import discord, os, json, asyncio
from discord.ext import commands 
from dotenv import load_dotenv
from pathlib import Path

FOLDER_DIR = Path(__file__).resolve().parent
print(FOLDER_DIR)
FILES = {
    "config": FOLDER_DIR / "storage/config.json"
}

with open(FILES["config"], "r") as file:
    config = json.load(file)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = commands.Bot(command_prefix=".")

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.playing, name="What is a cat, meow :3"))
    print ("*"*40)
    print ("Bot is ready to serve :D")
    print (f"Username: {client.user.name}")
    print (f"Bot version: {config["BOT_VERSION"]}")
    print ("*"*40)

cog_list = ['chat_bot', 'scam_detection', 'error_handling', 'server_status']
async def add_cogs():
    for cog in cog_list:
        await client.load_extension(f"cogs.{cog}")
        print(
            '*' * 20 
            + f" -> THE COG BY THE NAME: {cog}, LAUCHED <- " +
            '*' * 20 
        )

asyncio.run(add_cogs())

client.run(TOKEN, log_level=0)