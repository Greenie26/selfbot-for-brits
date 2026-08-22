import json, discord, io, base64, datetime
from discord.ext import commands
from helper_scripts.Ai_class import call_the_vl
from pathlib import Path
from PIL import Image

class Scam_detection(commands.Cog):
    def __init__(self, client):
        self.client = client

        FOLDER_DIR = Path().resolve()
        self.FILES = {
            "config": FOLDER_DIR / "storage/config.json"
        }
        with open(self.FILES["config"], mode="r") as file:
            self.config = json.load(file)
        self.ALLOWED_CHANNELS = list(self.config["ALLOWED_CHANNELS"].values())
        self.ALLOWED_ART_CHANNELS = list(self.config["ALLOWED_ART_CHANNELS"].values())
        self.ping_messages = {}

    async def check_for_whitelist(self, ctx):
        whitelisted_roles = self.config["WHITELISTED_ROLES"].values()
        whitelisted_people = self.config["WHITELISTED_PEOPLE"].values()
        for role in ctx.author.roles:
            if role.id in whitelisted_roles:
                return True

        if ctx.author.id in whitelisted_people:
            return True
        return False

#decided to play with output a bit, make it more "fun"
    def log_to_console(self, filepath: str, module_name: str, text: str):
        time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{time}] [{filepath}] [{module_name}] {text}")

    @commands.command()
    async def get_notified(self, ctx):
        return
        if not await self.check_for_whitelist(ctx):
            await ctx.reply("my guy, you are not an admin :pray: :wilted_rose:", delete_after=5)
            return
        username = ctx.message.author.name
        userID = ctx.message.author.id

        with open(self.FILES["config"], "r") as file:
            config = json.load(file)
        config["ENROLLED_FOR_PING_PEOPLE"][username] = userID
        with open(self.FILES["config"], "w") as file:
            json.dump(config, file, indent=4)
        await ctx.reply("successfully added you to notification", delete_after=5)

    @commands.command()
    async def dont_get_notified(self, ctx: commands.Context):
        return
        if not await self.check_for_whitelist(ctx):
            await ctx.reply("my guy, you are not an admin :pray: :wilted_rose:", delete_after=5)
            return
        username = ctx.message.author.name

        with open(self.FILES["config"], "r") as file:
            config = json.load(file)
        config["ENROLLED_FOR_PING_PEOPLE"].pop(username, None)
        with open(self.FILES["config"], "w") as file:
            json.dump(config, file, indent=4)
        await ctx.reply("successfully removed you from notification", delete_after=5)
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.attachments:
            #if message.author.id in list(config["WHITELISTED_PEOPLE"].values()):
            #    log_to_console((Path(__file__).name), "scam_detection", f"exempting {message.author.name} (id: {message.author.id}), because whitelisted")
            #    return 
        
            if message.channel.id not in self.ALLOWED_ART_CHANNELS:
                return
            
            flagged_reasons = []

            for file in message.attachments:
                self.log_to_console((Path(__file__).name), "scam_detection", f"Found image in {message.author.name}'s (id: {message.author.id}) message (message_id: {message.id})")
                if file.content_type and file.content_type.startswith('image/'):
                    #this was written by ai, cause i'm again, too stupid
                    raw_data = await file.read()
                    img = Image.open(io.BytesIO(raw_data)).convert('RGB')
                    img.thumbnail((512, 512)) 
                    buffer = io.BytesIO()
                    img.save(buffer, format='JPEG', quality=85)
                    base64cleaned = base64.b64encode(buffer.getvalue()).decode('utf-8')

                    verdict = await call_the_vl(base64cleaned)
                    print(verdict)
                    if not verdict:
                        self.log_to_console((Path(__file__).name), "scam_detection", "MAJOR AI FUCKUP!")
                    print(
                        "\n" + "=" * 50 + "\n"
                        f"[{Path(__file__).name}] [scam_detection]\n"
                        f"Status    : {verdict}\n"
                        + "=" * 50
                    )

                    if "SCAM" in verdict.upper():
                        flagged_reasons.append(verdict)

                    try:
                        await message.channel.fetch_message(message.id)
                    except discord.NotFound:
                        self.log_to_console((Path(__file__).name), "scam_detection", "message was deleted before pinging, stopping")
                        return
            if flagged_reasons:

                ping_list = []
                pingable_ids = list(self.config["ENROLLED_FOR_PING_PEOPLE"].values())
                print(pingable_ids)

                if pingable_ids:
                    for pingable_id in pingable_ids:
                        ping_list.append(f"<@{pingable_id}>")
                    ping_list_ready = " ".join(ping_list)
                    pinged_message = await message.channel.send(
                        f"{ping_list_ready}\n"
                        f"-# admins/mods can use .get_notified to join pings, and .dont_get_notified to leave.\n"
                        f"-# P.S NONE of the images are getting logged anywhere. ||<@1002650457333841950>|| \n"
                    )
                else:
                    #pinged_message = await message.channel.send(
                    #    f"Admins/Mods can join pings .get_notified\n"
                    #    f"-# P.S NONE of the images are getting logged anywhere. ||<@1002650457333841950>|| \n"
                    #)
                    pinged_message = await message.channel.send("-# Pinging for possible scam. Testing for false positives as i switched llm, sorry if it's incorrect. ||<@1002650457333841950>||")
                self.ping_messages[message.id] = pinged_message
            else:
                self.log_to_console((Path(__file__).name), "scam_detection", "no scam detected, nice")
        
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.id in self.ping_messages:
            ping_message = self.ping_messages.pop(message.id)
            try:
                await ping_message.delete()
                self.log_to_console((Path(__file__).name), "scam_detection", f"deleting ping message as the pinged message {message.id} was deleted")
            except discord.NotFound:
                pass

async def setup(bot):
    await bot.add_cog(Scam_detection(bot))