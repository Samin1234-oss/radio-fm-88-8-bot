import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Set up intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
bot = commands.Bot(command_prefix="!", intents=intents)

# Stream URL
STREAM_URL = "https://radio.garden/api/ara/content/listen/2MrE9uJ6/channel.mp3"

# When bot is ready
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# Play command
@bot.command()
async def play(ctx):
    if ctx.author.voice is None:
        await ctx.send("Join a voice channel first!")
        return
    channel = ctx.author.voice.channel
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio(STREAM_URL))
    await ctx.send("📻 Playing FM 88.8")

# Stop command
@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("⏹️ Stopped playing.")

# Run bot
bot.run(TOKEN)
