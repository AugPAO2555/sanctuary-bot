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

    print("Bot Ready")


# ---------- HELP ----------

@bot.tree.command(name="help")
async def help_cmd(interaction: discord.Interaction):

    embed = discord.Embed(
        title="📖 Command Guide",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="🎮 Quest",
        value="""
/dailyquest
/process
""",
        inline=False
    )

    embed.add_field(
        name="📢 Server",
        value="""
/announce
/ping
/help
""",
        inline=False
    )

    embed.add_field(
        name="📩 Mail",
        value="""
/letter
/mailall
""",
        inline=False
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
topic="หัวข้อ",
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
        title="📢 Announcement",
        color=discord.Color.red()
    )

    embed.add_field(name="Topic",value=topic,inline=False)
    embed.add_field(name="Date",value=date,inline=False)
    embed.add_field(name="Message",value=message,inline=False)

    await interaction.response.send_message(embed=embed)


# ---------- LETTER ----------

@bot.tree.command(name="letter")
@app_commands.describe(
target="ผู้รับ",
message="ข้อความ"
)
async def letter(interaction: discord.Interaction,target:discord.Member,message:str):

    embed = discord.Embed(
        title="📬 Secret Letter",
        description=message,
        color=discord.Color.gold()
    )

    try:

        await target.send(embed=embed)

        await interaction.response.send_message(
        f"{APPROVED} : ส่งจดหมายแล้ว"
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
                title="📬 Server Mail",
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
        title="📜 Daily Quest",
        description=f"""
Mission : {quest['name']}

Progress : 0/{quest['goal']}
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
        title="⏳ Quest Progress",
        description=f"""
Mission : {quest['name']}

Progress : {progress}/{quest['goal']}
""",
        color=discord.Color.orange()
    )

    await interaction.response.send_message(embed=embed)


TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)