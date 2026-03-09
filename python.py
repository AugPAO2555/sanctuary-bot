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

ALLOWED_USER = 996318050682937395

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
# HELP COMMAND
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
  - -# **/set-economy**
  - -# **/set-mail**
  - -# **/set-tarot**
  - -# **/songkran_login**
  - -# **/ping**

```ยังเป็นระบบเบต้าอยู่คำสั่งเลยน้อย แต่จะพยายามใส่เข้ามาเพิ่มให้ได้เล่นกันนะคั้บ ( อย่าลืมเข้าดิสเพื่อเช็ค update )```
""",
        color=0x2f3136
    )

    await interaction.response.send_message(embed=embed)

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
# PING
# ========================

@bot.tree.command(name="ping", description="ตรวจสอบสถานะบอท")
async def ping(interaction: discord.Interaction):

    latency = round(bot.latency * 1000)

    await interaction.response.send_message(
        f"Pong! 🏓\nLatency: {latency}ms"
    )

# ========================
# SONGKRAN LOGIN
# ========================

@bot.tree.command(name="songkran_login", description="💦 Songkran Login Event")
async def songkran_login(interaction: discord.Interaction):

    if interaction.user.id != ALLOWED_USER:
        await interaction.response.send_message("❌ คำสั่งนี้ใช้ได้เฉพาะเจ้าของบอท", ephemeral=True)
        return

    now = datetime.now(thai_tz)

    if not (now.month == 4 and 9 <= now.day <= 15):
        await interaction.response.send_message(
            "💦 Event นี้ใช้ได้เฉพาะช่วง **9-15 เมษายน** เท่านั้น",
            ephemeral=True
        )
        return

    user_id = interaction.user.id

    if user_id not in songkran_data:
        songkran_data[user_id] = {
            "points": 0,
            "day": 1
        }

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
            f"       ⵌ ได้รับ 1 point\n"
            f"       ⵌ ล็อคอินต่อเนื่องเพื่อรับรางวัล\n\n"
            f"__**🔥 Points Streaks**__\n"
            f"<:Water_Gun:1478767447413624842> {data['points']}"
        ),
        color=0x00bfff
    )

    embed.set_image(url=DAY_IMAGES.get(current_day, DAY_IMAGES[1]))

    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)