import discord
from discord.ext import tasks, commands

description = "Solo Squad Bot"
token = ""

msg_id = 925940075085320192
server_id = 925927824521572502

intents = discord.Intents.default()
intents.members = True

owners = [260813303029301249, 198267924039860235]

bot = commands.Bot(command_prefix='!', owner_ids = set(owners), description=description, intents=intents)

@bot.event
async def on_ready():
    print(str(bot.user.name) + " || " + str(bot.user.id))

@bot.event
async def on_raw_reaction_add(payload=None):
    msgID = msg_id
    guild = discord.utils.get(bot.guilds, id=server_id)
    twisted_role = discord.utils.get(guild.roles, name='Chambers of Xeric')
    tob_role = discord.utils.get(guild.roles, name='Theatre of Blood')
    nex_role = discord.utils.get(guild.roles, name='Nex')
    iron_role = discord.utils.get(guild.roles, name='Ironman')
    hcim_role = discord.utils.get(guild.roles, name='Hardcore Ironman')
    uim_role = discord.utils.get(guild.roles, name='Ultimate Ironman')
    infernal_role = discord.utils.get(guild.roles, name='Inferno Cape')
    quest_cape_role = discord.utils.get(guild.roles, name='Quest Cape')

    if payload is not None:
        if payload.message_id == msgID:
            if str(payload.emoji) == emoji.emojize('<:twisted:926295867105898496>'):
                await payload.member.add_roles(twisted_role)
            elif str(payload.emoji) == emoji.emojize('<:tob:926299912000401418>'):
                await payload.member.add_roles(tob_role)
            elif str(payload.emoji) == emoji.emojize('<:nex:926300474276196384>'):
                await payload.member.add_roles(nex_role)
            elif str(payload.emoji) == emoji.emojize('<:iron:926301101005889586>'):
                await payload.member.add_roles(iron_role)
            elif str(payload.emoji) == emoji.emojize('<:hcim:926300962916798514>'):
                await payload.member.add_roles(hcim_role)
            elif str(payload.emoji) == emoji.emojize('<:uim:926301036988227674>'):
                await payload.member.add_roles(uim_role)
            elif str(payload.emoji) == emoji.emojize('<:infernal:926301444557135902>'):
                await payload.member.add_roles(infernal_role)
            elif str(payload.emoji) == emoji.emojize('<:quest_cape:926300731454132226>'):
                await payload.member.add_roles(quest_cape_role)

@bot.event
async def on_raw_reaction_remove(payload=None):
    msgID = msg_id
    guild = discord.utils.get(bot.guilds, id=server_id)
    twisted_role = discord.utils.get(guild.roles, name='Chambers of Xeric')
    tob_role = discord.utils.get(guild.roles, name='Theatre of Blood')
    nex_role = discord.utils.get(guild.roles, name='Nex')
    iron_role = discord.utils.get(guild.roles, name='Ironman')
    hcim_role = discord.utils.get(guild.roles, name='Hardcore Ironman')
    uim_role = discord.utils.get(guild.roles, name='Ultimate Ironman')
    infernal_role = discord.utils.get(guild.roles, name='Inferno Cape')
    quest_cape_role = discord.utils.get(guild.roles, name='Quest Cape')

    if payload is not None:
        if payload.message_id == msgID:
            member = await guild.fetch_member(payload.user_id)
            if str(payload.emoji) == emoji.emojize('<:twisted:926295867105898496>'):
                await member.remove_roles(twisted_role)
            elif str(payload.emoji) == emoji.emojize('<:tob:926299912000401418>'):
                await member.remove_roles(tob_role)
            elif str(payload.emoji) == emoji.emojize('<:nex:926300474276196384>'):
                await member.remove_roles(nex_role)
            elif str(payload.emoji) == emoji.emojize('<:iron:926301101005889586>'):
                await member.remove_roles(iron_role)
            elif str(payload.emoji) == emoji.emojize('<:hcim:926300962916798514>'):
                await member.remove_roles(hcim_role)
            elif str(payload.emoji) == emoji.emojize('<:uim:926301036988227674>'):
                await member.remove_roles(uim_role)
            elif str(payload.emoji) == emoji.emojize('<:infernal:926301444557135902>'):
                await member.remove_roles(infernal_role)
            elif str(payload.emoji) == emoji.emojize('<:quest_cape:926300731454132226>'):
                await member.remove_roles(quest_cape_role)

bot.load_extension('cogs.TempleOSRS')
bot.load_extension('cogs.Admin')
bot.load_extension('cogs.Tasks')
bot.run(token)
