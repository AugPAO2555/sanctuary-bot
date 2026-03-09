import discord
from discord.ext import commands
from discord import app_commands
import os
import asyncio
from datetime import datetime, timedelta, timezone

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# ========================
# ICONS
# ========================

LETTER_ICON = "https://cdn.discordapp.com/attachments/1293404792814571552/1478335298898362368/121_20260303171623.png"
MAILBOX_ICON = "https://cdn.discordapp.com/attachments/1293404792814571552/1478333313038160072/120_20260303170821.png"

# Songkran Images
DAY_IMAGES = {
    1: "https://cdn.discordapp.com/attachments/1293404792814571552/1478771150661357639/126_20260304220611.jpg",
    2: "https://cdn.discordapp.com/attachments/1293404792814571552/1478771186421731418/126_20260304220631.jpg",
    3: "https://cdn.discordapp.com/attachments/1293404792814571552/1478771229774053398/126_20260304220648.jpg",
    4: "https://cdn.discordapp.com/attachments/1293404792814571552/1478771297621115022/126_20260304220657.jpg",
    5: "https://cdn.discordapp.com/attachments/1293404792814571552/1478771339257974914/126_20260304220706.jpg",
    6: "https://cdn.discordapp.com/attachments/1293404792814571552/1478771369310289941/126_20260304220712.jpg",
    7: "https://cdn.discordapp.com/attachments/1293404792814571552/1478771401484931184/126_20260304220717.jpg",
}

# เวลาไทย
thai_tz = timezone(timedelta(hours=7))
songkran_data = {}

# ========================
# BOT READY
# ========================
@bot.event
async def on_ready():
    print("=================================")
    print(f"Bot online: {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print("Sync error:", e)

    print("=================================")

# ========================
# VIEW เปิดจดหมาย
# ========================
class OpenLetterView(discord.ui.View):
    def __init__(self, content: str, sender_name: str):
        super().__init__(timeout=None)
        self.content = content
        self.sender_name = sender_name

    @discord.ui.button(label="เปิดจดหมาย", emoji="📩", style=discord.ButtonStyle.primary)
    async def open_letter(self, interaction: discord.Interaction, button: discord.ui.Button):

        embed = discord.Embed(
            description=f"﹒ˇ﹒__**You Got a Letter!**__ ﹒₊ ˚\n\n>>> {self.content}",
            color=0x2f3136
        )

        embed.set_author(
            name="Sanctuary Frontier Mail",
            icon_url=LETTER_ICON
        )

        embed.set_footer(
            text=f"﹒from : {self.sender_name}﹒ㆍ﹒"
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

# ========================
# /ping
# ========================
@bot.tree.command(name="ping", description="ตรวจสอบสถานะบอท")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"Pong! 🏓\nLatency: {latency}ms")

# ========================
# /songkran_login
# ========================
@bot.tree.command(name="songkran_login", description="💦 Songkran Daily Login")
async def songkran_login(interaction: discord.Interaction):

    user_id = interaction.user.id
    today = datetime.now(thai_tz).date()

    if user_id not in songkran_data:
        songkran_data[user_id] = {"last_login": None, "streak": 0}

    data = songkran_data[user_id]

    if data["last_login"] == today:
        embed = discord.Embed(description="💦 วันนี้คุณรับไปแล้ว!", color=0xffcc00)
        embed.set_image(url=DAY_IMAGES.get(data["streak"], DAY_IMAGES[1]))
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    if data["last_login"] == today - timedelta(days=1):
        data["streak"] += 1
    else:
        data["streak"] = 1

    if data["streak"] > 7:
        data["streak"] = 7

    data["last_login"] = today
    current_day = data["streak"]

    embed = discord.Embed(
        description=(
            f"﹒ˇ﹒{interaction.user.mention}﹒₊ ˚\n"
            f"﹒       __**Daily Log In**__﹒ㆍ﹒\n"
            f"       ⵌ ได้รับ 1 point\n"
            f"       ⵌ ล็อคอินต่อเนื่องเพื่อรับรางวัล\n\n"
            f"__**🔥 Points Streaks**__\n"
            f"<:Water_Gun:1478767447413624842> {current_day}"
        ),
        color=0x00bfff
    )

    embed.set_image(url=DAY_IMAGES.get(current_day, DAY_IMAGES[1]))

    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)