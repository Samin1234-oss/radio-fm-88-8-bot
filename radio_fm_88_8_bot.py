import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

# Set intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# FM Stream URL
STREAM_URL = "https://radio.garden/api/ara/content/listen/2MrE9uJ6/channel.mp3"

# ===== EVENTS =====
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# ===== COMMANDS =====

@bot.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("❌ Join a voice channel first!")
        return
    channel = ctx.author.voice.channel
    if ctx.voice_client is None or not ctx.voice_client.is_connected():
        await channel.connect()
        await ctx.send(f"✅ Joined {channel.name}")
    else:
        await ctx.send("❌ I'm already in a voice channel!")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("⏹️ Left the voice channel.")
    else:
        await ctx.send("❌ I'm not in a voice channel.")

@bot.command()
async def play(ctx):
    if ctx.author.voice is None:
        await ctx.send("❌ Join a voice channel first!")
        return
    if ctx.voice_client is None or not ctx.voice_client.is_connected():
        vc = await ctx.author.voice.channel.connect()
    else:
        vc = ctx.voice_client

    if not vc.is_playing():
        # Use the local ffmpeg binary
        vc.play(discord.FFmpegPCMAudio(STREAM_URL))
        await ctx.send("📻 Playing FM 88.8")
    else:
        await ctx.send("❌ Already playing!")

@bot.command()
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏹️ Stopped playing.")
    else:
        await ctx.send("❌ Nothing is playing.")

@bot.command()
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("⏸️ Paused.")
    else:
        await ctx.send("❌ Nothing is playing to pause.")

@bot.command()
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("▶️ Resumed.")
    else:
        await ctx.send("❌ Nothing is paused.")

@bot.command()
async def ffmpeg_test(ctx):
    import shutil
    if shutil.which("./ffmpeg"):
        await ctx.send("✅ FFmpeg binary found!")
    else:
        await ctx.send("❌ FFmpeg binary missing!")

# ===== RUN BOT =====
bot.run(TOKEN)

