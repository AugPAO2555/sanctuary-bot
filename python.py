import discord
from discord.ext import commands
from discord import app_commands
import json
import random
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

USER_FILE = "users.json"

APPROVED = "<:approved:1319887481403084854>"
DENIED = "<:denied:1319887409864900608>"

# --------- Status ----------

@bot.tree.command(name="status", description="ดูสถานะผู้เล่น")
async def status(interaction: discord.Interaction, target: discord.Member = None):

    users = load_users()

    if target is None:
        target = interaction.user

    uid = str(target.id)

    if uid not in users:
        users[uid] = {
            "uid": f"2026-{str(len(users)+1).zfill(5)}",
            "level": 1,
            "exp": 0,
            "gold": 0,
            "gem": 0
        }
        save_users(users)

    user = users[uid]

    # progress bar
    exp = user["exp"]
    bar_filled = int((exp / 10) * 10)
    bar = "█" * bar_filled + "░" * (10 - bar_filled)

    embed = discord.Embed(
        description=f"""
* __**‹ Status!**__ ⁺˖ ⸝⸝ 

▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

  - -# **❮ Username | ชื่อผู้ใช้บัญชีดิสคอร์ด ❯** :
  {target.name}

  - -# **❮ UID ❯** : {user['uid']}

  - -# **❮ Level | เลเวล ❯** : {user['level']}

  - -# **❮ Exp | ค่าประสบการณ์ ❯** : {user['exp']}
  {bar} ({user['exp']}/10)

  - -# **❮ Gold | เงิน ❯** : {user['gold']}

  - -# **❮ Gem | เพชร ❯** : {user['gem']}

▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
""",
        color=discord.Color.blurple()
    )

    embed.set_thumbnail(url=target.display_avatar.url)

    await interaction.response.send_message(embed=embed)

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

# ---------- QUESTS ----------

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

# ---------- HELP ----------

@bot.tree.command(name="help", description="Help Desk")
async def help_cmd(interaction: discord.Interaction):

    embed = discord.Embed(
        description="""
_ _
_ _ _ _ _ _ _ _ _ _ ﹒ㆍ__**Help-desk**__ ﹒ㆍ﹒ _ _
~~                                 ~~
_ _
* คำสั่งหลัก!
  - -# **/set-economy**
  - -# **/set-mail**
  - -# **/set-tarot**
  - -# **/reset**

* คำสั่งเฉพาะแอดมิน!


```ยังเป็นระบบเบต้าอยู่คำสั่งเลยน้อย แต่จะพยายามใส่เข้ามาเพิ่มให้ได้เล่นกันนะคั้บ ( อย่าลืมเข้าดิสเพื่อเช็ค update )```
""",
        color=discord.Color.blue()
    )

    embed.set_footer(
        text=f"Help requested by {interaction.user}",
        icon_url=interaction.user.display_avatar.url
    )

    await interaction.response.send_message(embed=embed)

# ---------- PING ----------

@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):

    latency = round(bot.latency * 1000)

    embed = discord.Embed(
        title="🏓 Pong",
        description=f"Latency : {latency} ms",
        color=discord.Color.green()
    )

    await interaction.response.send_message(embed=embed)

# ---------- ANNOUNCE ----------

@bot.tree.command(name="announce")
@app_commands.describe(
topic="หัวข้อประกาศ",
date="วันที่",
message="รายละเอียด"
)
async def announce(interaction: discord.Interaction,topic:str,date:str,message:str):

    if not interaction.user.guild_permissions.administrator:

        await interaction.response.send_message(
        f"{DENIED} : คุณไม่มีสิทธิ์ใช้คำสั่งนี้",
        ephemeral=True
        )

        return

    embed = discord.Embed(
        description=f"""
ㅤㅤㅤㅤㅤㅤㅤ❮ ประชาสัมพันธ์ <:GameZone_Full_Logo:1475409495856386139> ❯ㅤㅤㅤㅤㅤㅤㅤ

▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

( Topic | หัวข้อ ) : {topic}
( Date | วันที่ ) : {date}

{message}

▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
""",
        color=discord.Color.red()
    )

    embed.set_footer(
        text=f"Send by {interaction.user}",
        icon_url=interaction.user.display_avatar.url
    )

    await interaction.response.send_message(embed=embed)

# ---------- LETTER ----------

@bot.tree.command(name="letter")
@app_commands.describe(target="ผู้รับ",message="ข้อความ")
async def letter(interaction: discord.Interaction,target:discord.Member,message:str):

    embed = discord.Embed(
        title="Sanctuary Frontier Mail",
        description=f"""
﹒ˇ﹒__**Secret Sealed Just for You**__ ﹒₊ ˚

✉️ **มีใครบางคนแอบส่งจดหมายถึงคุณ...**

{message}
""",
        color=discord.Color.gold()
    )

    try:

        await target.send(embed=embed)

        await interaction.response.send_message(
        f"{APPROVED} : ใช้คำสั่งเสร็จสิ้น !"
        )

    except:

        await interaction.response.send_message(
        f"{DENIED} : ไม่สามารถส่ง DM ได้",
        ephemeral=True
        )

# ---------- MAIL ALL ----------

@bot.tree.command(name="mailall")
@app_commands.describe(message="ข้อความ")
async def mailall(interaction: discord.Interaction,message:str):

    if not interaction.user.guild_permissions.administrator:

        await interaction.response.send_message(
        f"{DENIED} : คุณไม่มีสิทธิ์ใช้คำสั่งนี้",
        ephemeral=True
        )

        return

    count = 0

    for member in interaction.guild.members:

        if member.bot:
            continue

        try:

            embed = discord.Embed(
                title="Sanctuary Frontier Mail",
                description=message,
                color=discord.Color.orange()
            )

            await member.send(embed=embed)

            count += 1

        except:
            pass

    await interaction.response.send_message(
    f"{APPROVED} : ส่งแล้ว {count} คน"
    )

# ---------- DAILY QUEST ----------

@bot.tree.command(name="dailyquest")
async def dailyquest(interaction: discord.Interaction):

    users = load_users()
    uid = str(interaction.user.id)

    if uid not in users:

        users[uid] = {"quest":None,"progress":0}

    if users[uid]["quest"]:

        await interaction.response.send_message(
        f"{DENIED} : คุณมีเควสอยู่แล้ว",
        ephemeral=True
        )

        return

    quest = random.choice(QUESTS)

    users[uid]["quest"] = quest
    users[uid]["progress"] = 0

    save_users(users)

    embed = discord.Embed(
        description=f"""
﹒ㆍ﹒__**Quest System!**__﹒ㆍ﹒

{APPROVED}﹕ __**รับเควสเรียบร้อย!**__

```{quest['name']}```

- -# **︶︶︶︶︶︶︶︶︶**
""",
        color=discord.Color.green()
    )

    await interaction.response.send_message(embed=embed)

# ---------- PROCESS ----------

@bot.tree.command(name="process")
async def process(interaction: discord.Interaction):

    users = load_users()
    uid = str(interaction.user.id)

    if uid not in users or not users[uid]["quest"]:

        await interaction.response.send_message(
        f"{DENIED} : คุณยังไม่มีเควส",
        ephemeral=True
        )

        return

    quest = users[uid]["quest"]
    progress = users[uid]["progress"]

    embed = discord.Embed(
        description=f"""
* __**‹ Quest-Process !**__ ⁺˖ ⸝⸝ 

﹒ ㆍ**{interaction.user.name}**﹒ㆍ

- -# ** ❮ Quest | เควส ❯** : {quest['name']}
- -# ** ❮ Progress | ความคืบหน้า ❯ **

({progress}/{quest['goal']})
""",
        color=discord.Color.orange()
    )

    await interaction.response.send_message(embed=embed)

# ---------- QUEST TRACKERS ----------

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    users = load_users()
    uid = str(message.author.id)

    if uid in users and users[uid]["quest"]:

        quest = users[uid]["quest"]

        if quest["type"] == "message":

            users[uid]["progress"] += 1

    save_users(users)

    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction,user):

    if user.bot:
        return

    users = load_users()
    uid = str(user.id)

    if uid in users and users[uid]["quest"]:

        quest = users[uid]["quest"]

        if quest["type"] == "reaction":

            users[uid]["progress"] += 1

    save_users(users)

TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)