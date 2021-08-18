import discord
from discord.ext import commands


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Commands

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(F"{round(self.bot.latency * 1000)}ms")


def setup(bot):
    bot.add_cog(Basic(bot))
