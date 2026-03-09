import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

STREAM_URL = "https://radio.garden/api/ara/content/listen/2MrE9uJ6/channel.mp3"

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def play(ctx):
    if ctx.author.voice is None:
        await ctx.send("Join a voice channel first!")
        return

    channel = ctx.author.voice.channel
    vc = await channel.connect()

    vc.play(discord.FFmpegPCMAudio(STREAM_URL))
    await ctx.send("📻 Playing FM 88.8")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()

bot.run(TOKEN)