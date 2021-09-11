import discord
from discord.ext import commands
import json
import random
import aiohttp
from typing import Optional as opt


def is_online(self):
    if self.status == discord.Status.online:
        return True


message = "Hey, what's going on. Chat looking awfully dead huh?"

discord.Member.is_online = is_online


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Commands

    # Displays a random anime quote
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

    # Shows if a member is online
    @commands.command(name="is_online", aliases=["io"])
    async def check_status(self, ctx, member: discord.Member):
        if member.is_online():
            await ctx.send('member online')
        else:
            await ctx.send('member not online')

    # Pings random online members
    @commands.command(name="randping", aliases=["rp"])
    @commands.has_permissions(manage_guild=True)
    async def rand_ping(self, ctx,  to_ping: opt[int] = 1,
                        msg: opt[str] = message):
        online_members = [member.mention for member in ctx.guild.members
                          if member.is_online() if not member.bot]
        ping_list = random.sample(online_members, to_ping)
        await ctx.send(' '.join(ping_list) + ' ' + msg)


def setup(bot):
    bot.add_cog(Fun(bot))
