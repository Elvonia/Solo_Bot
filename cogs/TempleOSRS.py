import discord
import requests
import json
import emoji
from discord.ext import tasks, commands
from requests.exceptions import HTTPError

class TempleOSRS(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.key = ""
        self.id = ""
        self.base_url = "https://templeosrs.com/api"
        self.add_member_url = "/add_group_member.php"
        self.rem_member_url = "/remove_group_member.php"
        print('[__init__ :: cogs.TempleOSRS]')

    @commands.command(pass_context=True)
    @commands.has_any_role('Admin','General')
    async def add(self, ctx, *, players):
        """Adds a user to the TempleOSRS group.

        Multiple users can be added in a single command by
        separating them with a comma.

        i.e. `add User1,User2,User3
        """
        self.editGroupMember(self.id, players, self.key, self.add_member_url)
        print("[Command: add] [User: " + ctx.message.author.name + "] Added: " + players)
        await ctx.send("Added: " + players)

    @commands.command(pass_context=True)
    @commands.has_any_role('Admin','General')
    async def remove(self, ctx, *, players):
        """Removes a user from the TempleOSRS group.

        Multiple users can be removed in a single command by
        separating them with a comma.

        i.e. `remove User1,User2,User3
        """
        self.editGroupMember(self.id, players, self.key, self.rem_member_url)
        print("[Command: remove] [User: " + ctx.message.author.name + "] Removed: " + players)
        await ctx.send("Removed: " + players)

    def editGroupMember(self, id, players, key, endpoint):
        data = {'id':id,'players':players,'key':key}
        self.templePostRequest(data, endpoint)

    def templePostRequest(self, data, endpoint):
        try:
            r = requests.post(self.base_url + endpoint, data=data)
            r.raise_for_status()

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Error occurred: {err}')


def setup(bot):
    bot.add_cog(TempleOSRS(bot))
