import discord
import os
from discord.ext import commands


PREFIX = 'mai '
INTENTS = discord.Intents().all()
TOKEN = os.environ['TOKEN']
bot = commands.Bot(command_prefix=PREFIX, intents=INTENTS)


@bot.event
async def on_ready:
    print('bot online')

bot.run(TOKEN)
