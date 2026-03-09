import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load token from .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Enable intents for commands (default is fine for voice)
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Radio stream URL
STREAM_URL = "https://radio.garden/api/ara/content/listen/2MrE9uJ6/channel.mp3"

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# Join command
@bot.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("⚠️ You must be in a voice channel first!")
        return
    channel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()
    await ctx.send(f"✅ Joined {channel}")

# Play command
@bot.command()
async def play(ctx):
    if ctx.voice_client is None:
        if ctx.author.voice is None:
            await ctx.send("⚠️ Join a voice channel first!")
            return
        channel = ctx.author.voice.channel
        vc = await channel.connect()
    else:
        vc = ctx.voice_client

    # Play the radio stream
    vc.stop()
    vc.play(discord.FFmpegPCMAudio(STREAM_URL, executable="./ffmpeg"))
    await ctx.send("📻 Playing FM 88.8")

# Leave command
@bot.command()
async def leave(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Left the voice channel")
    else:
        await ctx.send("⚠️ I am not in a voice channel")

bot.run(TOKEN)
