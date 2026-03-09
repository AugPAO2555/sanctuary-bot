import discord
from discord.ext import commands
from discord import app_commands
import os
from datetime import datetime, timedelta, timezone

TOKEN = os.getenv("TOKEN")

OWNER_ID = 996318050682937395

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
# READY
# ========================

@bot.event
async def on_ready():
    print("Bot Online:", bot.user)

    try:
        synced = await bot.tree.sync()
        print("Commands synced:", len(synced))
    except Exception as e:
        print("Sync error:", e)

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

@bot.tree.command(name="ping", description="Ping Bot")
async def ping(interaction: discord.Interaction):

    latency = round(bot.latency * 1000)

    await interaction.response.send_message(
        f"Pong 🏓 {latency}ms"
    )

# ========================
# STATUS
# ========================

@bot.tree.command(name="status", description="Player Status")
async def status(interaction: discord.Interaction):

    embed = discord.Embed(
        description=f"""
╭────────〔 Player Status 〕────────╮

👤 Username : {interaction.user.name}
🆔 UID : 2026-00001

💰 Money : 0
💎 Gems : 0

⭐ Level : 1
📊 EXP : 0 / 100
▱▱▱▱▱▱▱▱▱▱

────────────────

📜 Quest

Quest 1 : ส่งข้อความในดิส 10 ข้อความ
Process
• ▰▰▱▱▱▱▱▱▱▱ (2/10)

Rewards
• 50 EXP

────────────────

Quest 2 : อยู่ในห้อง VC 30 นาที

Process
• ▰▱▱▱▱▱▱▱▱▱ (3/30)

Rewards
• 100 EXP
• 2 Gems

╰──────────────────────────────╯
""",
        color=0x2f3136
    )

    embed.set_thumbnail(url=interaction.user.display_avatar.url)

    await interaction.response.send_message(embed=embed)

# ========================
# LETTER BUTTON
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

@bot.tree.command(name="letter", description="Send Letter")
async def letter(interaction: discord.Interaction, user: discord.Member, message: str):

    view = OpenLetterView(message, interaction.user.name)

    embed = discord.Embed(
        description="📬 คุณได้รับจดหมายใหม่",
        color=0x2f3136
    )

    embed.set_thumbnail(url=MAILBOX_ICON)

    await user.send(embed=embed, view=view)

    await interaction.response.send_message(
        ":aprove: : ใช้คำสั่งเสร็จสิ้น !",
        ephemeral=True
    )

# ========================
# MAIL ALL
# ========================

@bot.tree.command(name="mail_all", description="Mail Everyone")
async def mail_all(interaction: discord.Interaction, message: str):

    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("Owner only", ephemeral=True)
        return

    for member in interaction.guild.members:

        if member.bot:
            continue

        try:

            view = OpenLetterView(message, interaction.user.name)

            embed = discord.Embed(
                description="📬 คุณได้รับจดหมายจากระบบ",
                color=0x2f3136
            )

            embed.set_thumbnail(url=MAILBOX_ICON)

            await member.send(embed=embed, view=view)

        except:
            pass

    await interaction.response.send_message(
        ":aprove: : ใช้คำสั่งเสร็จสิ้น !",
        ephemeral=True
    )

# ========================
# ANNOUNCE
# ========================

@bot.tree.command(name="announce", description="Announcement")
async def announce(interaction: discord.Interaction, topic: str, date: str, detail: str):

    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("Owner only", ephemeral=True)
        return

    embed = discord.Embed(
        description=f"""
ㅤㅤㅤㅤㅤㅤㅤ❮ ประชาสัมพันธ์ <:GameZone_Full_Logo:1475409495856386139> ❯ㅤㅤㅤㅤㅤㅤㅤ

▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

( Topic | หัวข้อ ) : {topic}
( Date | วันที่ ) : {date}

{detail}

▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
""",
        color=0x2f3136
    )

    await interaction.channel.send(embed=embed)

    await interaction.response.send_message(
        ":aprove: : ใช้คำสั่งเสร็จสิ้น !",
        ephemeral=True
    )

# ========================
# SONGKRAN LOGIN
# ========================

@bot.tree.command(name="songkran_login", description="Songkran Event")
async def songkran_login(interaction: discord.Interaction):

    now = datetime.now(thai_tz)

    if interaction.user.id != OWNER_ID:
        if not (now.month == 4 and 9 <= now.day <= 15):

            await interaction.response.send_message(
                "💦 Event ใช้ได้เฉพาะ 9-15 เมษายน",
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
        description=f"""
﹒ˇ﹒{interaction.user.mention}﹒₊ ˚
﹒       __**Daily Log In**__﹒ㆍ﹒

ⵌ ได้รับ 1 point

🔥 Points Streaks
<:Water_Gun:1478767447413624842> {data['points']}
""",
        color=0x00bfff
    )

    embed.set_image(url=DAY_IMAGES.get(current_day, DAY_IMAGES[1]))

    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)