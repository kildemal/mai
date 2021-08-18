import discord
from discord.ext import commands
import json
import aiohttp


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Commands

    @commands.command()
    async def aniquote(self, ctx):
        async with aiohttp.ClientSession() as session:

            url = "https://animechan.vercel.app/api/random"
            async with session.get(url) as response:
                json_data = await response.json()
                quote = ("_'" + json_data['quote'] + "'_" + ' - ' +
                         json_data['character'] + ', **' + json_data['anime'] +
                         '**')

        await ctx.send(quote)


def setup(bot):
    bot.add_cog(Fun(bot))
