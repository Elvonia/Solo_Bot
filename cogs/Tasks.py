import discord
import json
import random
import emoji
from discord.ext import tasks, commands

class Tasks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('[__init__ :: cogs.Tasks]')


    @commands.command(pass_context=True)
    async def task(self, ctx):
        """Command for generating a random combat task."""
        f = open('tasks.json')
        j = json.load(f)

        rng = random.randint(0, 194)
        msg = await ctx.send(j[rng]["Task"])
        await msg.add_reaction(emoji.emojize('<:quest_cape:926300731454132226>'))


def setup(bot):
    bot.add_cog(Tasks(bot))