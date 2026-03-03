import discord
from discord.ext import commands
from discord import app_commands
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# ========================
# ตรวจสอบ permission
# ========================
def has_announce_permission(user: discord.Member):
    if user.guild_permissions.administrator:
        return True

    allowed_roles = ["Admin", "Moderator", "Mod", "Staff"]
    return any(role.name in allowed_roles for role in user.roles)

# ========================
# เมื่อ bot online
# ========================
@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands synced: {len(synced)}")
    except Exception as e:
        print(e)

# ========================
# /ping
# ========================
@bot.tree.command(name="ping", description="ตรวจสอบสถานะบอท")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(
        f"Pong! 🏓\nLatency: {latency}ms"
    )

# ========================
# /announce
# ========================
@bot.tree.command(name="announce", description="สร้างประกาศประชาสัมพันธ์")
@app_commands.describe(
    topic="หัวข้อประกาศ",
    date="วันที่",
    content="เนื้อหาประกาศ"
)
async def announce(interaction: discord.Interaction, topic: str, date: str, content: str):

    if not has_announce_permission(interaction.user):
        await interaction.response.send_message(
            "❌ เฉพาะ Admin หรือ Mod เท่านั้น",
            ephemeral=True
        )
        return

    LOGO = "<:GameZone_Full_Logo:1475409495856386139>"
    LINE = "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬"

    embed = discord.Embed(
        description=(
            f"ㅤㅤㅤㅤㅤㅤㅤ❮ ประชาสัมพันธ์ {LOGO} ❯ㅤㅤㅤㅤㅤㅤㅤ\n\n"
            f"{LINE}\n\n"
            f"( Topic | หัวข้อ ) : {topic}\n"
            f"( Date | วันที่ ) : {date}\n\n"
            f"{content}\n\n"
            f"{LINE}"
        ),
        color=0x2f3136
    )

    embed.set_footer(
        text=f"ประกาศโดย {interaction.user.display_name}",
        icon_url=interaction.user.display_avatar.url
    )

    await interaction.response.send_message(embed=embed)

# ========================
# ระบบจดหมาย
# ========================

LETTER_ICON = "https://cdn.discordapp.com/attachments/1293404792814571552/1478335298898362368/121_20260303171623.png"

class OpenLetterView(discord.ui.View):
    def __init__(self, content: str, sender_name: str):
        super().__init__(timeout=None)
        self.content = content
        self.sender_name = sender_name

    @discord.ui.button(label="เปิดจดหมาย", emoji="📩", style=discord.ButtonStyle.primary)
    async def open_letter(self, interaction: discord.Interaction, button: discord.ui.Button):

        embed = discord.Embed(
            description=(
                "﹒ˇ﹒__**Surprise! It’s..just bills**__ ﹒₊ ˚\n"
                f"-# **เปิดซองออกมา... ไม่ใช่จดหมายรัก แต่เป็นใบแจ้งหนี้แทน 😭 "
                f"( {self.content} )**"
            ),
            color=0xe74c3c
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
# /letter command
# ========================
@bot.tree.command(name="letter", description="ส่งจดหมายลับถึงเพื่อน")
@app_commands.describe(
    user="ผู้รับจดหมาย",
    content="ข้อความในจดหมาย"
)
async def letter(interaction: discord.Interaction, user: discord.Member, content: str):

    embed = discord.Embed(
        description=(
            "﹒ˇ﹒__**Secret Sealed Just for You**__ ﹒₊ ˚\n\n"
            "<:dns_c2o8:1369689361926328420> "
            "**มีใครบางคนแอบส่งจดหมายถึงคุณ...**"
        ),
        color=0x2f3136
    )

    embed.set_author(
        name="Sanctuary Frontier Mail",
        icon_url=LETTER_ICON
    )

    embed.set_footer(
        text=f"﹒dear : {user.name}﹒ㆍ﹒",
        icon_url=user.display_avatar.url
    )

    view = OpenLetterView(content, interaction.user.name)

    await interaction.response.send_message("📨 ส่งจดหมายเรียบร้อยแล้ว!", ephemeral=True)
    await user.send(embed=embed, view=view)

# ========================
# Run bot
# ========================
bot.run(TOKEN)
