import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import os

# --- WEB SERVER (Uyumaması için) ---
app = Flask('')
@app.route('/')
def home():
    return "Bot 7/24 Aktif!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- BOT KODU ---
TOKEN = 'BURAYA_TOKENINI_YAZ'
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

active_staff = []

@bot.event
async def on_ready():
    print(f'{bot.user} sahada!')

@bot.command()
async def online(ctx):
    if ctx.author.id not in active_staff:
        active_staff.append(ctx.author.id)
        await ctx.send(f"✅ {ctx.author.mention} sıraya girdi.")
    else:
        await ctx.send("Zaten sıradasın.")

@bot.command()
async def offline(ctx):
    if ctx.author.id in active_staff:
        active_staff.remove(ctx.author.id)
        await ctx.send(f"❌ {ctx.author.mention} sıradan çıktı.")

@bot.event
async def on_guild_channel_create(channel):
    if channel.name.startswith('ticket-'):
        if not active_staff:
            await channel.send("⚠️ Online satışçı yok! @Vision")
            return

        assigned_id = active_staff.pop(0)
        active_staff.append(assigned_id)
        
        await channel.send(f"🔔 Yeni Müşteri! Sıra sende: <@{assigned_id}>")

keep_alive() # Web server'ı başlat
bot.run(TOKEN)