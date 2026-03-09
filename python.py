import discord
from discord.ext import commands
from discord import app_commands
import json
import random
import os

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

USER_FILE = "users.json"

QUEST_CHANNEL = 1461916719894499573

APPROVED = "<:approved:1319887481403084854>"
DENIED = "<:denied:1319887409864900608>"

# ---------- JSON ----------

def load_users():
    try:
        with open(USER_FILE,"r") as f:
            return json.load(f)
    except:
        return {}

def save_users(data):
    with open(USER_FILE,"w") as f:
        json.dump(data,f,indent=4)

def create_user(uid):

    users = load_users()

    if uid not in users:

        users[uid] = {
            "level":1,
            "exp":0,
            "gold":0,
            "gem":0,
            "quest":None,
            "progress":0
        }

        save_users(users)

    return users

# ---------- QUEST LIST ----------

QUESTS = [

{"name":"Send 5 messages","type":"message","goal":5},

{"name":"React to a message","type":"reaction","goal":1},

{"name":"Mention a member","type":"mention","goal":1}

]

# ---------- READY ----------

@bot.event
async def on_ready():

    await bot.tree.sync()

    print(f"Bot Online : {bot.user}")

# ---------- PROGRESS BAR ----------

def progress_bar(progress, goal):

    percent = progress/goal
    filled = int(percent*10)

    return "▰"*filled + "▱"*(10-filled)

# ---------- QUEST COMPLETE ----------

async def quest_complete(user, quest):

    users = load_users()
    uid = str(user.id)

    users[uid]["gold"] += 10
    users[uid]["exp"] += 10

    if users[uid]["exp"] >= 10:

        users[uid]["exp"] = 0
        users[uid]["level"] += 1

    users[uid]["quest"] = None
    users[uid]["progress"] = 0

    save_users(users)

    channel = bot.get_channel(QUEST_CHANNEL)

    if channel:

        await channel.send(f"""
<:Wing1:1319892658835034195> **⊹˚ ︵‿︵‿︵‿︵‿︵‿︵‿︵‿︵‿︵‿︵ ˚⊹** <:Wing2:1319892647938232341>

<:notification:1420605475594043484>「QUEST SYSTEM ANNOUNCEMENT」<:notification:1420605475594043484>

ท่านผู้กล้า : {user.mention}! ได้สำเร็จเควส **"{quest['name']}"**

ได้รับรางวัล
- **10 Gold**
- **10 Exp**

<:Wing1:1319892658835034195> **⊹˚ ︵‿︵‿︵‿︵‿︵‿︵‿︵‿︵‿︵‿︵ ˚⊹** <:Wing2:1319892647938232341>
""")

# ---------- STATUS ----------

@bot.tree.command(name="status")
async def status(interaction: discord.Interaction,target:discord.Member=None):

    if not target:
        target = interaction.user

    uid = str(target.id)

    users = create_user(uid)

    user = users[uid]

    bar = progress_bar(user["exp"],10)

    embed = discord.Embed(
        description=f"""
* __**‹ Status!**__ ⁺˖ ⸝⸝ 

▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

- **Username**
{target}

- **UID**
{target.id}

- **Level**
{user['level']}

- **Exp**
{user['exp']}
{bar} ({user['exp']}/10)

- **Gold**
{user['gold']}

- **Gem**
{user['gem']}

▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
""",
        color=discord.Color.blurple()
    )

    await interaction.response.send_message(embed=embed)

# ---------- HELP ----------

@bot.tree.command(name="help")
async def help(interaction:discord.Interaction):

    embed=discord.Embed(
        title="Bot Commands",
        description="""
/status — ดูสถานะ
/dailyquest — รับเควสรายวัน
/process — ดู progress เควส
/letter — ส่งจดหมาย
/help — รายการคำสั่ง
""",
        color=discord.Color.green()
    )

    await interaction.response.send_message(embed=embed)

# ---------- LETTER VIEW ----------

class LetterView(discord.ui.View):

    def __init__(self,message,sender):

        super().__init__(timeout=None)
        self.message=message
        self.sender=sender

    @discord.ui.button(label="Open Letter",emoji="✉️",style=discord.ButtonStyle.primary)
    async def open_letter(self,interaction:discord.Interaction,button:discord.ui.Button):

        await interaction.response.send_message(f"""
﹒ˇ﹒__**Surprise! It’s..just bills**__ ﹒₊ ˚

**{self.message}**

send by {self.sender.mention}
""",ephemeral=True)

# ---------- LETTER ----------

@bot.tree.command(name="letter")
async def letter(interaction:discord.Interaction,target:discord.Member,message:str):

    embed=discord.Embed(
        title="Sanctuary Frontier Mail",
        description=f"""
Secret Sealed Just for You

✉️ มีจดหมายถึงคุณ

Dear {target.mention}
""",
        color=discord.Color.gold()
    )

    view=LetterView(message,interaction.user)

    await interaction.response.send_message(
        content=target.mention,
        embed=embed,
        view=view
    )

# ---------- DAILY QUEST ----------

@bot.tree.command(name="dailyquest")
async def dailyquest(interaction:discord.Interaction):

    uid=str(interaction.user.id)

    users=create_user(uid)

    if users[uid]["quest"]:

        await interaction.response.send_message(
        f"{DENIED} คุณมีเควสอยู่แล้ว",
        ephemeral=True
        )
        return

    quest=random.choice(QUESTS)

    users[uid]["quest"]=quest
    users[uid]["progress"]=0

    save_users(users)

    await interaction.response.send_message(
    f"{APPROVED} รับเควส **{quest['name']}** แล้ว!"
    )

# ---------- PROCESS ----------

@bot.tree.command(name="process")
async def process(interaction:discord.Interaction):

    uid=str(interaction.user.id)

    users=create_user(uid)

    if not users[uid]["quest"]:

        await interaction.response.send_message(
        f"{DENIED} คุณยังไม่มีเควส",
        ephemeral=True
        )
        return

    quest=users[uid]["quest"]
    progress=users[uid]["progress"]

    bar=progress_bar(progress,quest["goal"])

    embed=discord.Embed(
        description=f"""
‹ Quest Process ›

Quest
{quest['name']}

Progress
{bar} ({progress}/{quest['goal']})
""",
        color=discord.Color.orange()
    )

    await interaction.response.send_message(embed=embed)

# ---------- QUEST TRACKERS ----------

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    users=load_users()
    uid=str(message.author.id)

    if uid in users and users[uid]["quest"]:

        quest=users[uid]["quest"]

        # MESSAGE QUEST
        if quest["type"]=="message":

            users[uid]["progress"]+=1

        # MENTION QUEST
        elif quest["type"]=="mention":

            if message.mentions:

                if message.mentions[0] != message.author:

                    users[uid]["progress"]+=1

        if users[uid]["progress"]>=quest["goal"]:

            await quest_complete(message.author,quest)

    save_users(users)

    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction,user):

    if user.bot:
        return

    users=load_users()
    uid=str(user.id)

    if uid in users and users[uid]["quest"]:

        quest=users[uid]["quest"]

        if quest["type"]=="reaction":

            users[uid]["progress"]+=1

            if users[uid]["progress"]>=quest["goal"]:

                await quest_complete(user,quest)

    save_users(users)

# ---------- RUN ----------

TOKEN=os.getenv("TOKEN")

bot.run(TOKEN)