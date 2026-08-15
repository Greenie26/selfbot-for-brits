import time, ServerPinging, json, discord, io, base64
from discord.ext import commands
from Ai_class import call_the_chat, call_the_vl
from pathlib import Path
from PIL import Image

FOLDER_DIR = Path(__file__).resolve().parent
print(FOLDER_DIR)
FILES = {
    "question_logger": FOLDER_DIR / "QaA.txt",
    "questions": FOLDER_DIR / "QuestionRequests.txt",
    "config": FOLDER_DIR / "config.json"
}
#made a config to clean up variables, probably made it even more cluttered, but i had to play with it :D
with open(FILES["config"], "r") as file:
    config = json.load(file)

TOKEN = config["TOKEN"]
ALLOWED_CHANNELS = list(config["ALLOWED_CHANNELS"].values())
 
client = commands.Bot(command_prefix=".")

sent_messages = []
timeout_until = 0
ping_messages = {}

GUILD_ID = config["TARGET_GUILD_ID"]
BOT_IDS = config["BOT_IDS"]
# ----------------
def format_delay(delay_list: list[bool, int], max_ping):
    if delay_list[1] >= max_ping and delay_list[0]:
        return f"| delay {delay_list[1]}ms, Higher than usual"
    elif delay_list[1] < max_ping and delay_list[0]:
        return f"| delay {delay_list[1]}ms, Normal"
    elif not delay_list[0]:
        return ""
# ----------------    
async def get_bots():
    GUILD = await client.fetch_guild(GUILD_ID)
    members = await GUILD.query_members(
            user_ids=[
                int(BOT_IDS["USbotID"]),
                int(BOT_IDS["EUbotID"]),
                int(BOT_IDS["AUbotID"])
                ],
            presences=True,
            subscribe=True
        )
    return members
# ----------------
def format_status(status_string: str, min_players:int):
    if "Offline" in status_string:
        return status_string

    player = int(status_string.split()[0])
    if player < min_players:
        return f"{player} players online | playercount abnormally low"
    return status_string
# ----------------

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.playing, name="What is a cat, meow :3"))
    print ("*"*40)
    print ("Bot is ready to serve :D")
    print (f"Username: {client.user.name}")
    print ("*"*40)


@client.command()
async def status(ctx: commands.Context):
    global sent_messages, timeout_until

    if ctx.channel.id not in ALLOWED_CHANNELS:
        return
    
    #dunno where to put this clunky code, don't know how to make it into a function 3:
    now = time.time()
    if now < timeout_until:
        remaining = round(timeout_until - now, 1)
        await ctx.channel.send(f"timeout: wait {remaining} seconds until typing again", delete_after=4)
        return
    sent_messages = [(t, msg) for t, msg in sent_messages if now - t < 10]
    if len(sent_messages) >= 3:
        timeout_until = now + 15
        for _, msg in sent_messages:
            try:
                await msg.delete()
            except Exception:
                pass
        sent_messages.clear()
        await ctx.channel.send("timeout: wait 15.0 seconds until typing again", delete_after=4)
        return
    
    # load bots so they won't equal to None when you search for them
    print(f"[{Path(__file__).name}] [status] Loading specific bots into memory...")

    members = await get_bots()
    
    print(f"[{Path(__file__).name}] [status] Bots loaded!")

    USBOT = next((member for member in members if member.id == int(BOT_IDS["USbotID"])), None)
    EUBOT = next((member for member in members if member.id == int(BOT_IDS["EUbotID"])), None)
    AUBOT = next((member for member in members if member.id == int(BOT_IDS["AUbotID"])), None)

    UsStatus = format_status(USBOT.activity.name, 50) 
    EuStatus = format_status(EUBOT.activity.name, 50)
    AuStatus = format_status(AUBOT.activity.name, 10)

    USWorldsDelay =  format_delay(ServerPinging.get_us_delay(), 150)
    EUWorldsDelay =  format_delay(ServerPinging.get_eu_delay(), 250)
    AUWorldsDelay =  format_delay(ServerPinging.get_au_delay(), 320)

    print(f"[{Path(__file__).name}] [status] Proccessed everything correctly")

    sent_msg = await ctx.message.reply(
        f"US status - {UsStatus} {USWorldsDelay}\n"
        f"EU status - {EuStatus} {EUWorldsDelay}\n"
        f"AU status - {AuStatus} {AUWorldsDelay}\n"
        f"-# Delays are for client that is located at Southeastern region of USA",
        mention_author=True
    )   
    sent_messages.append((now, sent_msg))
    print(f"[{Path(__file__).name}] [status] sent a message correctly")

@client.command()
async def question(ctx: commands.Context):
    askinguser = ctx.author.name
    question = ctx.message.content
    try:
        answer = call_the_chat(ctx.message.content.split(None, 1)[1])
        await ctx.message.reply(answer)
    except IndexError:
        await ctx.message.reply("You need to prove a question.")
        answer= "You need to prove a question."
    with open(FILES["question_logger"], "a", encoding="utf-8") as file:
        file.write(f"{askinguser}\n{question}\n{answer}\n---------\n")
    print(f"[{Path(__file__).name}] [question] wrote to the {Path(FILES['question_logger']).name} file")

@client.command()
async def submit_question(ctx: commands.Context):
    reason = ctx.message.content.split(None, 1)[1]
    with open(FILES["questions"], "a", encoding="utf-8") as file:
        file.write(f"{reason}\n---------\n")
    print(f"[{Path(__file__).name}] [submit_question] wrote to the {Path(FILES['questions']).name} file ")

@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.attachments:
        #if message.author.id in list(config["WHITELISTED_PEOPLE"].values()):
        #    print(f"[{Path(__file__).name}] [scam_detection] exempting {message.author.name} (id: {message.author.id}), because whitelisted")
        #    return 
    
        if message.channel.id not in ALLOWED_CHANNELS:
            return
        
        flagged_reasons = []
        for file in message.attachments:
            if file.content_type and file.content_type.startswith('image/'):
                print(f"[{Path(__file__).name}] [scam_detection] Found image in {message.author.name}'s (id: {message.author.id}) message (message_id: {message.id})")

                #this was written by ai, cause i'm again, too stupid
                raw_data = await file.read()
                img = Image.open(io.BytesIO(raw_data)).convert('RGB')
                img.thumbnail((512, 512)) 
                buffer = io.BytesIO()
                img.save(buffer, format='JPEG', quality=85)
                base64cleaned = base64.b64encode(buffer.getvalue()).decode('utf-8')

                verdict = call_the_vl(base64cleaned)
                verdictwords = verdict.split("|")
                verdict_status = verdictwords[0].strip()
                verdict_reason = verdictwords[1].strip() 

                print(
                    "\n" + "=" * 50 + "\n"
                    f"[{Path(__file__).name}] [scam_detection]\n"
                    f"Status    : {verdict_status}\n"
                    f"Reasoning : {verdict_reason}\n"
                    + "=" * 50
                )
                if "SCAM" in verdict_status.upper():
                    flagged_reasons.append(verdict_status)
        print(f"\n[{Path(__file__).name}] [scam_detection] If scam present ({verdict_status}), giving a ping.\n")
        if flagged_reasons:
            pinged_message = await message.channel.send(
                f"<@1002650457333841950>\n"
                f"-# pinging for the reason that image(s) above seem like a scam, sorry if it's incorrect, i'm testing to minimize false positives.\n"
                f"-# P.S NONE of the images are getting logged anywhere.\n"
            )
            ping_messages[message.id] = pinged_message
    else:
        return
    
@client.event
async def on_message_delete( message):
    if message.id in ping_messages:
        ping_message = ping_messages.pop(message.id)
        await ping_message.delete()
        print(f"[{Path(__file__).name}] [scam_detection] deleting ping message as the pinged message {message.id} was deleted")

client.run(TOKEN)