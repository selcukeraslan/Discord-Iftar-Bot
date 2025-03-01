import discord
from discord.ext import commands
import requests
from datetime import datetime

TOKEN = "YOUR_BOT_TOKEN"  # Buraya kendi Discord bot token'ını gir
API_URL = "https://vakit.vercel.app/api/timesFromPlace?country=Turkey&region=Istanbul&city=Istanbul"

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"{bot.user.name} olarak giriş yapıldı.")

@bot.command()
async def iftar(ctx):
    try:
        response = requests.get(API_URL)
        data = response.json()
        
        today = datetime.now().strftime("%Y-%m-%d")
        iftar_time = None

        for item in data['data']['times']:
            if item['date'] == today:
                iftar_time_str = item['maghrib']
                iftar_time = datetime.strptime(f"{today} {iftar_time_str}", "%Y-%m-%d %H:%M")
                break

        if not iftar_time:
            await ctx.send("Bugünün iftar saati bulunamadı.")
            return

        now = datetime.now()
        time_left = iftar_time - now

        if time_left.total_seconds() < 0:
            await ctx.send("İftar vakti geçti.")
        else:
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            await ctx.send(f"İftara {hours} saat, {minutes} dakika, {seconds} saniye kaldı.")

    except Exception as e:
        await ctx.send("Bir hata oluştu.")
        print(e)

bot.run(TOKEN)
