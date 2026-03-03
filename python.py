import discord
from discord.ext import commands
from discord import app_commands
import os
import asyncio

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# ========================
# /mailall ส่ง DM ทุกคน
# ========================
@bot.tree.command(name="mailall", description="ส่งจดหมายถึงสมาชิกทุกคนในเซิร์ฟเวอร์")
@app_commands.describe(content="ข้อความในจดหมาย")
async def mailall(interaction: discord.Interaction, content: str):

    # อนุญาตเฉพาะแอดมิน
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "❌ ใช้ได้เฉพาะแอดมิน",
            ephemeral=True
        )
        return

    await interaction.response.send_message(
        "📨 เริ่มกระบวนการส่งจดหมาย...",
        ephemeral=True
    )

    members = [m for m in interaction.guild.members if not m.bot]
    total = len(members)

    success = 0
    failed = 0

    progress_msg = await interaction.followup.send(f"กำลังส่ง 0/{total}")

    for index, member in enumerate(members, start=1):
        try:
            embed = discord.Embed(
                description=(
                    "﹒ˇ﹒__**Secret Sealed Just for You**__ ﹒₊ ˚\n\n"
                    "<:dns_c2o8:1369689361926328420> "
                    "**มีใครบางคนแอบส่งจดหมายถึงคุณ...**\n\n"
                    f">>> {content}"
                ),
                color=0x2f3136
            )

            embed.set_author(
                name="Sanctuary Frontier Mail",
                icon_url=LETTER_ICON
            )

            embed.set_footer(
                text=f"จากทีมงาน • {interaction.guild.name}",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )

            await member.send(embed=embed)
            success += 1

        except:
            failed += 1

        # อัปเดตทุก 5 คน
        if index % 5 == 0 or index == total:
            await progress_msg.edit(
                content=f"กำลังส่ง {index}/{total}"
            )

        await asyncio.sleep(0.4)  # เหมาะกับ 216 คน

    await progress_msg.edit(
        content=(
            "✅ ส่งจดหมายครบแล้ว!\n"
            f"สำเร็จ: {success}\n"
            f"ส่งไม่ได้ (ปิด DM): {failed}"
        )
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
