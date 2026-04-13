import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import os

# --- RENDER İÇİN WEB SERVER ---
app = Flask('')
@app.route('/')
def home():
    return "EasyGlobal Bot Aktif!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    # daemon=True yaptık ki bot çökerse zombi gibi yaşamasın, Render hatayı anlasın!
    t = Thread(target=run, daemon=True)
    t.start()

# --- BOT MANTIĞI ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

active_staff = []

@bot.event
async def on_ready():
    print(f'BAŞARILI: {bot.user} sahaya indi!')

@bot.command()
async def online(ctx):
    if ctx.author.id not in active_staff:
        active_staff.append(ctx.author.id)
        await ctx.send(f"✅ {ctx.author.mention} satış sırasına girdi.")
    else:
        await ctx.send("Zaten sıradasın kanka.")

@bot.command()
async def offline(ctx):
    if ctx.author.id in active_staff:
        active_staff.remove(ctx.author.id)
        await ctx.send(f"❌ {ctx.author.mention} sıradan çıktı.")

@bot.event
async def on_guild_channel_create(channel):
    if channel.name.startswith('ticket-'):
        if not active_staff:
            return 
        assigned_id = active_staff.pop(0)
        active_staff.append(assigned_id)
        await channel.send(f"🔔 Yeni Müşteri! Sıra sende: <@{assigned_id}>")

keep_alive()

# --- HATA YAKALAYICI (BİZİM AJAN) ---
token = os.environ.get('DISCORD_TOKEN')

if not token:
    print("--------------------------------------------------")
    print("KRİTİK HATA: DISCORD_TOKEN bulunamadı!")
    print("Render'da Environment Variables kısmına tokeni girmemişsin veya ismini yanlış yazmışsın.")
    print("--------------------------------------------------")
else:
    try:
        bot.run(token)
    except discord.errors.PrivilegedIntentsRequired:
        print("--------------------------------------------------")
        print("KRİTİK HATA: Discord Developer Portal'dan yetkileri (Intents) açmamışsın kanka!")
        print("Portalda 'Bot' sekmesine girip 3 tane Intent ayarını mavi (açık) yap.")
        print("--------------------------------------------------")
    except discord.errors.LoginFailure:
        print("--------------------------------------------------")
        print("KRİTİK HATA: Token yanlış! Developer Portal'dan yanlış şeyi kopyalamışsın.")
        print("--------------------------------------------------")
    except Exception as e:
        print(f"BİLİNMEYEN HATA: {e}")
