import discord
from discord.ext import commands
from discord import app_commands
import os
from datetime import datetime, timedelta, timezone

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

OWNER_ID = 996318050682937395

# ========================
# ICONS
# ========================

LETTER_ICON = "https://cdn.discordapp.com/attachments/1293404792814571552/1478335298898362368/121_20260303171623.png"
MAILBOX_ICON = "https://cdn.discordapp.com/attachments/1293404792814571552/1478333313038160072/120_20260303170821.png"

DAY_IMAGES = {
    1: "https://cdn.discordapp.com/attachments/1293404792814571552/1478771150661357639/126_20260304220611.jpg",
    2: "https://cdn.discordapp.com/attachments/1293404792814571552/1478771186421731418/126_20260304220631.jpg",
    3: "https://cdn.discordapp.com/attachments/1293404792814571552/1478771229774053398/126_20260304220648.jpg",
    4: "https://cdn.discordapp.com/attachments/1293404792814571552/1478771297621115022/126_20260304220657.jpg",
    5: "https://cdn.discordapp.com/attachments/1293404792814571552/1478771339257974914/126_20260304220706.jpg",
    6: "https://cdn.discordapp.com/attachments/1293404792814571552/1478771369310289941/126_20260304220712.jpg",
    7: "https://cdn.discordapp.com/attachments/1293404792814571552/1478771401484931184/126_20260304220717.jpg",
}

thai_tz = timezone(timedelta(hours=7))
songkran_data = {}

# ========================
# BOT READY
# ========================

@bot.event
async def on_ready():
    print("============================")
    print(f"Bot online: {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print("Sync error:", e)

    print("============================")

# ========================
# HELP
# ========================

@bot.tree.command(name="help", description="Help Desk")
async def help_cmd(interaction: discord.Interaction):

    embed = discord.Embed(
        description="""
_ _
_ _ _ _ _ _ _ _ _ _  ﹒ㆍ__**Help-desk**__ ﹒ㆍ﹒ _ _
~~                                 ~~
_ _

* Main Command !
  - -# **/ping**
  - -# **/status**
  - -# **/letter**
  - -# **/mail_all**
  - -# **/announce**
  - -# **/songkran_login**

```ยังเป็นระบบเบต้าอยู่คำสั่งเลยน้อย แต่จะพยายามใส่เข้ามาเพิ่มให้ได้เล่นกันนะคั้บ ( อย่าลืมเข้าดิสเพื่อเช็ค update )```
""",
        color=0x2f3136
    )

    await interaction.response.send_message(embed=embed)

# ========================
# PING
# ========================

@bot.tree.command(name="ping", description="ตรวจสอบสถานะบอท")
async def ping(interaction: discord.Interaction):

    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"Pong! 🏓\nLatency: {latency}ms")

# ========================
# STATUS
# ========================

@bot.tree.command(name="status", description="Player Status")
async def status(interaction: discord.Interaction):

    embed = discord.Embed(
        description=(
            f"👤 Username : {interaction.user.name}\n"
            f"🆔 UID : 2026-00001\n\n"
            f"💰 Money : 0\n"
            f"💎 Gems : 0\n\n"
            f"⭐ Level : 1\n"
            f"📊 EXP : 0 / 100"
        ),
        color=0x2f3136
    )

    embed.set_thumbnail(url=interaction.user.display_avatar.url)

    await interaction.response.send_message(embed=embed)

# ========================
# LETTER VIEW
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
# LETTER
# ========================

@bot.tree.command(name="letter", description="ส่งจดหมาย")
async def letter(interaction: discord.Interaction, user: discord.Member, message: str):

    view = OpenLetterView(message, interaction.user.name)

    embed = discord.Embed(
        description="📬 คุณได้รับจดหมายใหม่!",
        color=0x2f3136
    )

    embed.set_thumbnail(url=MAILBOX_ICON)

    await user.send(embed=embed, view=view)

    await interaction.response.send_message("📩 ส่งจดหมายแล้ว", ephemeral=True)

# ========================
# MAIL ALL
# ========================

@bot.tree.command(name="mail_all", description="ส่งจดหมายทุกคน")
async def mail_all(interaction: discord.Interaction, message: str):

    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("❌ Owner only", ephemeral=True)
        return

    for member in interaction.guild.members:

        if member.bot:
            continue

        try:
            view = OpenLetterView(message, interaction.user.name)

            embed = discord.Embed(
                description="📬 คุณได้รับจดหมายจากเซิร์ฟเวอร์!",
                color=0x2f3136
            )

            embed.set_thumbnail(url=MAILBOX_ICON)

            await member.send(embed=embed, view=view)

        except:
            pass

    await interaction.response.send_message("📨 ส่งจดหมายให้ทุกคนแล้ว", ephemeral=True)

# ========================
# ANNOUNCE
# ========================

@bot.tree.command(name="announce", description="ประกาศข้อความ")
async def announce(interaction: discord.Interaction, message: str):

    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("❌ Owner only", ephemeral=True)
        return

    embed = discord.Embed(
        title="📢 Announcement",
        description=message,
        color=0xff5555
    )

    await interaction.channel.send(embed=embed)

    await interaction.response.send_message("✅ ประกาศแล้ว", ephemeral=True)

# ========================
# SONGKRAN LOGIN
# ========================

@bot.tree.command(name="songkran_login", description="💦 Songkran Login Event")
async def songkran_login(interaction: discord.Interaction):

    now = datetime.now(thai_tz)

    if interaction.user.id != OWNER_ID:
        if not (now.month == 4 and 9 <= now.day <= 15):
            await interaction.response.send_message(
                "💦 Event นี้ใช้ได้เฉพาะช่วง **9-15 เมษายน**",
                ephemeral=True
            )
            return

    user_id = interaction.user.id

    if user_id not in songkran_data:
        songkran_data[user_id] = {"points": 0, "day": 1}

    data = songkran_data[user_id]

    data["points"] += 1
    data["day"] += 1

    if data["day"] > 7:
        data["day"] = 1
        data["points"] = 0

    current_day = data["day"]

    embed = discord.Embed(
        description=(
            f"﹒ˇ﹒{interaction.user.mention}﹒₊ ˚\n"
            f"﹒       __**Daily Log In**__﹒ㆍ﹒\n"
            f"       ⵌ ได้รับ 1 point\n\n"
            f"__**🔥 Points Streaks**__\n"
            f"<:Water_Gun:1478767447413624842> {data['points']}"
        ),
        color=0x00bfff
    )

    embed.set_image(url=DAY_IMAGES.get(current_day, DAY_IMAGES[1]))

    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)