import discord
from discord.ext import commands
import json
import random
import io
import aiohttp
from typing import Union, Optional as opt


# Returns true if member is online
def is_online(self):
    if self.status == discord.Status.online:
        return True


# Returns true if message content has no everyone or here
def no_everyone(self):
    return not any(m in self.message.content for m in ["@here", "@everyone"])


# The default message for the random ping function
message = "Hey, what's going on. Chat looking awfully dead huh?"

discord.Member.is_online = is_online  # Adds is_online() method to member object


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
                        *, msg: opt[str] = message):
        await ctx.message.delete()
        online_members = [member.mention for member in ctx.guild.members
                          if member.is_online() if not member.bot]
        ping_list = random.sample(online_members, to_ping)
        await ctx.send(' '.join(ping_list) + ' ' + msg)

    # Repeats the users message
    @commands.command(name="say")
    @commands.check(no_everyone)
    async def say(self, ctx, *, msg=None):
        await ctx.message.delete()
        if msg is not None:
            await ctx.send(msg)

    # Steals emojis
    @commands.command(name="steal_emoji", aliases=["se"])
    @commands.has_permissions(manage_emojis=True)
    async def steal_emoji(self, ctx,
                          *emoji: Union[discord.Emoji, discord.PartialEmoji]):
        created_emojis = []
        async with aiohttp.ClientSession() as session:
            for emj in emoji:
                async with session.get(str(emj.url)) as url:
                    img = await url.read()
                    created_emoji = await ctx.guild.create_custom_emoji(image=img, name=emj.name)
                    created_emojis.append(created_emoji)

        await session.close()
        await ctx.send(f'Succesfully created emoji: {" ".join(str(e) for e in created_emojis)}')

    # Adds emoji from url
    @commands.command(name="add_emoji", aliases=["ae"])
    @commands.has_permissions(manage_emojis=True)
    async def add_emoji(self, ctx, url: str, name: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(str(url)) as url:
                img = await url.read()
                emoji = await ctx.guild.create_custom_emoji(image=img, name=name)
        await session.close()
        await ctx.send(f'Succesfully created emoji: {emoji}')


def setup(bot):
    bot.add_cog(Fun(bot))
