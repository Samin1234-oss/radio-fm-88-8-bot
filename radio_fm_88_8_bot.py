import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# FM Stream URL
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
        await ctx.send("❌ Join a voice channel first!")
        return
    channel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)  # Move if bot is in another channel
    else:
        vc = await channel.connect()
    await ctx.send(f"✅ Joined {channel}")

# Play command
@bot.command()
async def play(ctx):
    global vc
    if ctx.author.voice is None:
        await ctx.send("❌ Join a voice channel first!")
        return
    if ctx.voice_client is None:
        vc = await ctx.author.voice.channel.connect()
    else:
        vc = ctx.voice_client
        if not vc.is_connected():
            vc = await ctx.author.voice.channel.connect()
    if not vc.is_playing():
        vc.play(discord.FFmpegPCMAudio(STREAM_URL))
        await ctx.send("📻 Playing FM 88.8")
    else:
        await ctx.send("Already playing!")

# Stop command
@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("⏹️ Stopped and left the channel.")
    else:
        await ctx.send("❌ I'm not in a voice channel.")

# Pause command
@bot.command()
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("⏸️ Paused the stream.")
    else:
        await ctx.send("❌ Nothing is playing!")

# Resume command
@bot.command()
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("▶️ Resumed the stream.")
    else:
        await ctx.send("❌ Nothing is paused!")

#Leave Command
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("⏹️ Left the channel.")
    else:
        await ctx.send("❌ I'm not in a voice channel.")

@bot.command()
async def ffmpeg_test(ctx):
    import shutil
    if shutil.which("ffmpeg"):
        await ctx.send("✅ FFmpeg is installed!")
    else:
        await ctx.send("❌ FFmpeg is missing!")

# Lease command (custom)
@bot.command()
async def lease(ctx):
    await ctx.send("✅ Bot is online and ready!")

# Run bot
bot.run(TOKEN)


