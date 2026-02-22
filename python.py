import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")

@bot.command()
async def hello(ctx):
    await ctx.send("Sanctuary Frontier Bot is now Online!")

bot.run(TOKEN)