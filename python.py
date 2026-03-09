import discord
from discord.ext import commands
from discord import app_commands
import json
import random
import datetime

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

QUEST_FILE = "quests.json"
USER_FILE = "users.json"

APPROVED = "<:approved:1319887481403084854>"
WAITING = "<:Waiting_for_approval:1393514897400135812>"
DENIED = "<:denied:1319887409864900608>"


def load(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {}


def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Bot Ready")


# รับเควสรายวัน
@bot.tree.command(name="dailyquest")
async def dailyquest(interaction: discord.Interaction):

    quests = load(QUEST_FILE)
    users = load(USER_FILE)

    uid = str(interaction.user.id)
    today = str(datetime.date.today())

    if uid not in users:
        users[uid] = {
            "completed": [],
            "current": None,
            "date": ""
        }

    if users[uid]["date"] == today:
        await interaction.response.send_message(
            f"{DENIED} คุณรับเควสวันนี้แล้ว",
            ephemeral=True
        )
        return

    available = [q for q in quests if q not in users[uid]["completed"]]

    if not available:
        users[uid]["completed"] = []
        available = list(quests.keys())

    quest = random.choice(available)

    users[uid]["current"] = quest
    users[uid]["date"] = today

    save(USER_FILE, users)

    await interaction.response.send_message(
        f"{WAITING} Daily Quest\n\n📜 {quest}"
    )


# ดูเควสที่กำลังทำ
@bot.tree.command(name="process")
async def process(interaction: discord.Interaction):

    users = load(USER_FILE)
    uid = str(interaction.user.id)

    if uid not in users or not users[uid]["current"]:
        await interaction.response.send_message(
            f"{DENIED} คุณยังไม่มีเควส",
            ephemeral=True
        )
        return

    quest = users[uid]["current"]

    await interaction.response.send_message(
        f"{WAITING} Quest in Progress\n\n📜 {quest}"
    )


# ส่งเควส
@bot.tree.command(name="complete")
async def complete(interaction: discord.Interaction):

    users = load(USER_FILE)
    uid = str(interaction.user.id)

    if uid not in users or not users[uid]["current"]:
        await interaction.response.send_message(
            f"{DENIED} ไม่มีเควสให้ส่ง",
            ephemeral=True
        )
        return

    quest = users[uid]["current"]

    users[uid]["completed"].append(quest)
    users[uid]["current"] = None

    save(USER_FILE, users)

    await interaction.response.send_message(
        f"{APPROVED} Quest Completed!\n📜 {quest}"
    )


# Owner เพิ่มเควส
@bot.tree.command(name="addquest")
@app_commands.describe(text="ชื่อเควส")
async def addquest(interaction: discord.Interaction, text: str):

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            f"{DENIED} Owner Only",
            ephemeral=True
        )
        return

    quests = load(QUEST_FILE)

    quests[text] = True

    save(QUEST_FILE, quests)

    await interaction.response.send_message(
        f"{APPROVED} เพิ่มเควสแล้ว\n📜 {text}"
    )


# Owner รีเซ็ตเควสผู้เล่น
@bot.tree.command(name="resetquest")
async def resetquest(interaction: discord.Interaction):

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            f"{DENIED} Owner Only",
            ephemeral=True
        )
        return

    save(USER_FILE, {})

    await interaction.response.send_message(
        f"{APPROVED} รีเซ็ตเควสทั้งหมดแล้ว"
    )


# ตรวจ Reaction
@bot.event
async def on_reaction_add(reaction, user):

    if user.bot:
        return

    users = load(USER_FILE)
    uid = str(user.id)

    if uid not in users:
        return

    if users[uid]["current"] != "React to any message":
        return

    users[uid]["completed"].append(users[uid]["current"])
    users[uid]["current"] = None

    save(USER_FILE, users)

    await reaction.message.channel.send(
        f"{APPROVED} {user.mention} Quest Completed!"
    )


bot.run("YOUR_BOT_TOKEN")