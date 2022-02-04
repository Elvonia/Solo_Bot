import discord
import asyncio
import glob
import os
from discord.ext import tasks, commands

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('[__init__ :: cogs.Admin]')


    @commands.command(pass_context=True, hidden=True)
    @commands.is_owner()
    async def eval(self, ctx, *, code):
        """Evaluates code."""
        def check(m):
            if m.content.strip().lower() == "more":
                return True

        author = ctx.message.author
        channel = ctx.message.channel

        code = code.strip('` ')
        result = None

        global_vars = globals().copy()
        global_vars['bot'] = self.bot
        global_vars['ctx'] = ctx
        global_vars['message'] = ctx.message
        global_vars['author'] = ctx.message.author
        global_vars['channel'] = ctx.message.channel
        global_vars['server'] = ctx.message.guild

        try:
            result = eval(code, global_vars, locals())
        except Exception as e:
            await ctx.send(self.box('{}: {}'.format(type(e).__name__, str(e)),
                                   lang="py"))
            return

        if asyncio.iscoroutine(result):
            result = await result

        result = str(result)
        result = list(self.pagify(result, shorten_by=16))

        for i, page in enumerate(result):
            if i != 0 and i % 4 == 0:
                last = await ctx.send("There are still {} messages. "
                                          "Type `more` to continue."
                                          "".format(len(result) - (i+1)))
                msg = await self.bot.wait_for_message(author=author,
                                                      channel=channel,
                                                      check=check,
                                                      timeout=10)
                if msg is None:
                    try:
                        await ctx.delete_message(last)
                    except:
                        pass
                    finally:
                        break
            await ctx.send(self.box(page, lang="py"))


    @commands.group(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def delete(self, ctx):
        """Command group for deleting channel messages."""
        if ctx.invoked_subcommand is None:
            return


    @delete.command(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def after(self, ctx, message_id : int):
        """Deletes all messages in a channel after a specified id."""

        channel = ctx.message.channel
        author = ctx.message.author
        server = channel.guild
        is_bot = self.bot.user.bot
        has_permissions = channel.permissions_for(server.me).manage_messages

        to_delete = []

        after = await channel.fetch_message(message_id)

        if not has_permissions:
            await ctx.send("Missing manage_messages permission.")
            return
        elif not after:
            await ctx.send("Message not found.")
            return

        async for message in channel.history(limit=2000,
                                                after=after):
            to_delete.append(message)

        print("{} deleted {} messages in channel #{}"
                    "".format(author.name,
                              len(to_delete), channel.name))

        await self.mass_purge(channel, to_delete)


    @delete.command(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def messages(self, ctx, number: int):
        """Deletes specified amount of messages."""

        channel = ctx.message.channel
        author = ctx.message.author
        server = author.guild
        has_permissions = channel.permissions_for(server.me).manage_messages

        to_delete = []

        if not has_permissions:
            await self.bot.say("Missing manage_messages permission.")
            return

        async for message in channel.history(limit=number+1):
            to_delete.append(message)

        print("{} deleted {} messages in channel {}"
                    "".format(author.name,
                              number, channel.name))

        await self.mass_purge(channel, to_delete)
        

    async def mass_purge(self, channel, messages):
        while messages:
            if len(messages) > 1:
                await channel.delete_messages(messages[:100])
                messages = messages[100:]
            else:
                await channel.delete_messages(messages[0])
                messages = []
            await asyncio.sleep(1.5)


    def box(self, text, lang=""):
        ret = "```{}\n{}\n```".format(lang, text)
        return ret

    def escape(self, text, *, mass_mentions=False, formatting=False):
        if mass_mentions:
            text = text.replace("@everyone", "@\u200beveryone")
            text = text.replace("@here", "@\u200bhere")
        if formatting:
            text = (text.replace("`", "\\`")
                        .replace("*", "\\*")
                        .replace("_", "\\_")
                        .replace("~", "\\~"))
        return text


    def escape_mass_mentions(self, text):
        return self.escape(text, mass_mentions=True)

    def pagify(self, text, delims=["\n"], *, escape=True, shorten_by=8,
           page_length=2000):

        in_text = text
        if escape:
            num_mentions = text.count("@here") + text.count("@everyone")
            shorten_by += num_mentions
        page_length -= shorten_by
        while len(in_text) > page_length:
            closest_delim = max([in_text.rfind(d, 0, page_length)
                                 for d in delims])
            closest_delim = closest_delim if closest_delim != -1 else page_length
            if escape:
                to_send = escape_mass_mentions(in_text[:closest_delim])
            else:
                to_send = in_text[:closest_delim]
            yield to_send
            in_text = in_text[closest_delim:]

        if escape:
            yield self.escape_mass_mentions(in_text)
        else:
            yield in_text


def setup(bot):
    bot.add_cog(Admin(bot))