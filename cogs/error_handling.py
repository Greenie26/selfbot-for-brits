import json, discord, io, base64
from discord.ext import commands
from Ai_class import call_the_chat, call_the_vl
from pathlib import Path
from PIL import Image

class Error_handling(commands.Cog):
    def __init__(self, client):
        self.client = client
        
        FOLDER_DIR = Path().resolve()
        self.FILES = {
            "config": FOLDER_DIR / "storage/config.json"
        }

@commands.Cog.listener()
async def on_command_error(self, ctx: commands.Context, error):
    self.log_to_console((Path(__file__).name), "error", f"{error}")
    if isinstance(error, commands.CommandOnCooldown):
        remaining = round(error.retry_after, 1)
        await ctx.send(f"{ctx.author.mention} timeout: wait {remaining} seconds before typing again", delete_after=4)
        self.log_to_console((Path(__file__).name), "status", f"command went on cooldown for {remaining} seconds.")

@commands.Cog.listener()
async def on_command_error(self, ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error

async def setup(bot):
    await bot.add_cog(Error_handling(bot))