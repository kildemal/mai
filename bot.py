import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


PREFIX = '&'
INTENTS = discord.Intents().all()
TOKEN = os.environ.get('TOKEN')
bot = commands.Bot(command_prefix=PREFIX, intents=INTENTS)


@bot.event
async def on_ready():
    print('bot online')


# Funtions to manage loading of Cogs


@bot.command()  # Loads cogs
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")


@bot.command()  # Unloads cogs
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")


@bot.command()  # Reloads cogs
@commands.is_owner()
async def reload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")

# Loop to load cogs upon launch

for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(TOKEN)
