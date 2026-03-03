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

LETTER_ICON = "https://cdn.discordapp.com/attachments/1293404792814571552/1478335298898362368/121_20260303171623.png"

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
            description=(
                "﹒ˇ﹒__**You Got a Letter!**__ ﹒₊ ˚\n\n"
                f">>> {self.content}"
            ),
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

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "❌ เฉพาะ Admin เท่านั้น",
            ephemeral=True
        )
        return

    LINE = "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬"

    embed = discord.Embed(
        description=(
            f"❮ ประชาสัมพันธ์ ❯\n\n"
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
# /letter (ส่งรายบุคคล)
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
            "✉️ มีใครบางคนแอบส่งจดหมายถึงคุณ..."
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

    view = OpenLetterView(content, interaction.user.display_name)

    await interaction.response.send_message("📨 ส่งจดหมายเรียบร้อยแล้ว!", ephemeral=True)
    await user.send(embed=embed, view=view)

# ========================
# /mailall (Admin Only)
# ========================
@bot.tree.command(
    name="mailall",
    description="ส่งจดหมายถึงสมาชิกทุกคน (Admin Only)",
    default_permissions=discord.Permissions(administrator=True)
)
@app_commands.describe(content="ข้อความในจดหมาย")
async def mailall(interaction: discord.Interaction, content: str):

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
                    "✉️ มีใครบางคนแอบส่งจดหมายถึงคุณ..."
                ),
                color=0x2f3136
            )

            embed.set_author(
                name="Sanctuary Frontier Mail",
                icon_url=LETTER_ICON
            )

            embed.set_footer(
                text=f"﹒dear : {member.name}﹒ㆍ﹒",
                icon_url=member.display_avatar.url
            )

            view = OpenLetterView(content, interaction.user.display_name)

            await member.send(embed=embed, view=view)
            success += 1

        except:
            failed += 1

        if index % 5 == 0 or index == total:
            await progress_msg.edit(content=f"กำลังส่ง {index}/{total}")

        await asyncio.sleep(0.4)

    await progress_msg.edit(
        content=(
            "✅ ส่งจดหมายครบแล้ว!\n"
            f"สำเร็จ: {success}\n"
            f"ส่งไม่ได้ (ปิด DM): {failed}"
        )
    )

# ========================
# Run bot
# ========================
bot.run(TOKEN)
