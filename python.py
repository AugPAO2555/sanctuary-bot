import discord
from discord.ext import commands
from discord import app_commands
import json
import random
import datetime
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

QUEST_FILE = "quests.json"
USER_FILE = "users.json"

APPROVED = "<:approved:1319887481403084854>"
WAITING = "<:Waiting_for_approval:1393514897400135812>"
DENIED = "<:denied:1319887409864900608>"


# ---------------- JSON ----------------

def load(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# ---------------- RESPONSE SYSTEM ----------------

async def denied(interaction, text):
    await interaction.response.send_message(
        f"{DENIED} : {text}",
        ephemeral=True
    )


async def approved(interaction, text):
    await interaction.response.send_message(
        f"{APPROVED} : {text}"
    )


# ---------------- READY ----------------

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot Ready | {bot.user}")


# ---------------- PING ----------------

@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):

    latency = round(bot.latency * 1000)

    await interaction.response.send_message(
f"""
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
🏓 Pong

Latency : {latency} ms
System : Online
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
"""
    )


# ---------------- HELP ----------------

@bot.tree.command(name="help")
async def help_cmd(interaction: discord.Interaction):

    await interaction.response.send_message(
"""
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
📖 Command List

🎮 Quest
/dailyquest
/process
/complete
/cancelquest

📩 Mail
/letter
/mailall

📢 Server
/announce
/ping
/help
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
"""
    )


# ---------------- ANNOUNCE ----------------

@bot.tree.command(name="announce")
@app_commands.describe(
topic="หัวข้อ",
date="วันที่",
message="รายละเอียด"
)
async def announce(
interaction: discord.Interaction,
topic: str,
date: str,
message: str
):

    if not interaction.user.guild_permissions.administrator:
        await denied(interaction,"คุณไม่มีสิทธิ์ใช้คำสั่งประกาศ")
        return

    text = f"""
ㅤㅤㅤㅤㅤㅤㅤ❮ ประชาสัมพันธ์ ❯ㅤㅤㅤㅤㅤㅤㅤ

▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

( Topic | หัวข้อ ) : {topic}
( Date | วันที่ ) : {date}

{message}

▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
"""

    await interaction.response.send_message(text)


# ---------------- QUEST LIST ----------------

@bot.tree.command(name="questlist")
async def questlist(interaction: discord.Interaction):

    quests = load(QUEST_FILE)

    text = "\n".join([f"📜 {q}" for q in quests])

    await interaction.response.send_message(
f"""
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
📜 Quest List

{text}

▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
"""
    )


# ---------------- DAILY QUEST ----------------

@bot.tree.command(name="dailyquest")
async def dailyquest(interaction: discord.Interaction):

    quests = load(QUEST_FILE)
    users = load(USER_FILE)

    uid = str(interaction.user.id)
    today = str(datetime.date.today())

    if uid not in users:
        users[uid] = {"quests": [], "date": ""}

    if users[uid]["date"] == today:
        await denied(interaction,"คุณรับเควสวันนี้แล้ว")
        return

    quest = random.choice(list(quests.keys()))

    users[uid]["quests"].append(quest)
    users[uid]["date"] = today

    save(USER_FILE, users)

    await interaction.response.send_message(
f"""
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
📜 Daily Quest

Mission :
{quest}

Use /complete when finished
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
"""
    )


# ---------------- PROCESS ----------------

@bot.tree.command(name="process")
async def process(interaction: discord.Interaction):

    users = load(USER_FILE)
    uid = str(interaction.user.id)

    if uid not in users or not users[uid]["quests"]:
        await denied(interaction,"คุณยังไม่มีเควสที่กำลังดำเนินการ")
        return

    text = "\n".join([f"📜 {q}" for q in users[uid]["quests"]])

    await interaction.response.send_message(
f"""
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
⏳ Quest In Progress

{text}

▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
"""
    )


# ---------------- COMPLETE ----------------

@bot.tree.command(name="complete")
@app_commands.describe(quest="ชื่อเควส")
async def complete(interaction: discord.Interaction, quest: str):

    users = load(USER_FILE)
    uid = str(interaction.user.id)

    if uid not in users or quest not in users[uid]["quests"]:
        await denied(interaction,"ไม่พบเควสนี้ในรายการของคุณ")
        return

    users[uid]["quests"].remove(quest)

    save(USER_FILE, users)

    await approved(interaction,f"Quest Completed : {quest}")


# ---------------- CANCEL QUEST ----------------

@bot.tree.command(name="cancelquest")
@app_commands.describe(quest="ชื่อเควส")
async def cancelquest(interaction: discord.Interaction, quest: str):

    users = load(USER_FILE)
    uid = str(interaction.user.id)

    if uid not in users or quest not in users[uid]["quests"]:
        await denied(interaction,"ไม่พบเควสนี้")
        return

    users[uid]["quests"].remove(quest)

    save(USER_FILE, users)

    await approved(interaction,"ยกเลิกเควสสำเร็จ")


# ---------------- LETTER ----------------

@bot.tree.command(name="letter")
@app_commands.describe(target="ผู้รับ",message="ข้อความ")
async def letter(interaction: discord.Interaction,target: discord.Member,message: str):

    embed = discord.Embed(
        title="📬 Sanctuary Frontier Mail",
        description=f"""
﹒ˇ﹒__Secret Sealed Just for You__﹒

Dear {target.name}

{message}
""",
        color=discord.Color.gold()
    )

    try:

        await target.send(embed=embed)

        await approved(interaction,"ส่งจดหมายเรียบร้อย")

    except:

        await denied(interaction,"ไม่สามารถส่ง DM ได้")


# ---------------- MAIL ALL ----------------

@bot.tree.command(name="mailall")
@app_commands.describe(message="ข้อความ")
async def mailall(interaction: discord.Interaction,message: str):

    if not interaction.user.guild_permissions.administrator:
        await denied(interaction,"คุณไม่มีสิทธิ์ใช้คำสั่งนี้")
        return

    count = 0

    for member in interaction.guild.members:

        if member.bot:
            continue

        try:

            await member.send(message)

            count += 1

        except:
            pass

    await approved(interaction,f"ส่งจดหมายแล้ว {count} คน")


TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)