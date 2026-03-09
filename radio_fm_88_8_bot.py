import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Stream URL
STREAM_URL = "https://radio.garden/api/ara/content/listen/2MrE9uJ6/channel.mp3"

# Track voice client
vc = None

# Bot ready
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# Join command
@bot.command()
async def join(ctx):
    global vc
    if ctx.author.voice is None:
        await ctx.send("Join a voice channel first!")
        return
    channel = ctx.author.voice.channel
    vc = await channel.connect()
    await ctx.send(f"✅ Joined {channel}")

# Play command
@bot.command()
async def play(ctx):
    global vc
    if ctx.author.voice is None:
        await ctx.send("Join a voice channel first!")
        return
    if vc is None or not vc.is_connected():
        channel = ctx.author.voice.channel
        vc = await channel.connect()
    if not vc.is_playing():
        vc.play(discord.FFmpegPCMAudio(STREAM_URL))
        await ctx.send("📻 Playing FM 88.8")
    else:
        await ctx.send("Already playing!")

# Stop command
@bot.command()
async def stop(ctx):
    global vc
    if vc and vc.is_connected():
        await vc.disconnect()
        vc = None
        await ctx.send("⏹️ Stopped and left the channel.")
    else:
        await ctx.send("I'm not in a voice channel.")

# Pause command
@bot.command()
async def pause(ctx):
    if vc and vc.is_playing():
        vc.pause()
        await ctx.send("⏸️ Paused the stream.")
    else:
        await ctx.send("Nothing is playing!")

# Resume command
@bot.command()
async def resume(ctx):
    if vc and vc.is_paused():
        vc.resume()
        await ctx.send("▶️ Resumed the stream.")
    else:
        await ctx.send("Nothing is paused!")

# Lease command (custom)
@bot.command()
async def lease(ctx):
    await ctx.send("✅ Bot is online and ready!")

# Run bot
bot.run(TOKEN)
