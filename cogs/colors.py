import discord
from discord.ext import commands
import random


class Colors(commands.Cog):
    def init(self, bot):
        self.bot = bot

    # Events

    @commands.Cog.listener()
    async def on_member_join(self, member):
        color_roles = [x for x in member.guild.roles if x.name.endswith('🎨')]
        await member.add_roles(random.choice(color_roles))


def setup(bot):
    bot.add_cog(Colors(bot))
