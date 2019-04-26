import discord

from datetime import datetime 

from redbot.core import Config, checks, commands
from redbot.core.bot import Red

from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions

from . import create

from modmail import modmail
from tabulate import tabulate

async def please_wait_reply(author):
    # message = "Your message has been recieved. Someone will reply as soon as possible."
    message = "Thanks for helping."
    await author.send(message)

async def message_from_user_embed(message, author):
    # TODO: Handle attachments
    message_from_user = discord.Embed(
        description=(f"{message.content}")
    )
    message_from_user.set_author(
        name=f"{author.name}",
        icon_url=f"{author.avatar_url}"
    )
    return message_from_user

async def channel_finder(author, guild):
    for channel in guild.channels:
        if str(author.id) in channel.name:
            return channel


async def message_mods(bot, message, config):
    author = message.author
    author_config = await config.user(author).info()

    #if author_config['multi_guild_hold']:
    #    print("multi-hold")
    #    return

    #if author_config['is_waiting']:
    #    return await author.send("Your message has been recieved, please allow some time before sending another")

    user_is_blocked = await modmail.Modmail.is_user_blocked(author, config)
    if user_is_blocked:
        print(f"Blocked user attempted to message : {author.name}")
        return await author.send("You are have been blocked from sending ModMail messages.")

    # # channel_name = discord.utils.get(self.bot.guilds, id=556800157082058784)

    # Get a list of guilds the user & bot share
    guilds = [member.guild for member in bot.get_all_members()
              if member.id == author.id]

    if len(guilds) > 1:
        async with config.user(author).info() as info:
            info['multi_guild_hold'] = True

        table = [[index, guild.name] for index, guild in enumerate(guilds)]

        #for (index, guild) in enumerate(guilds):
        #    table = [[index, guild.name]]
        await author.send(
            "We have more than one server in common, please choose from list below where you would like to send the message.")
        msg = await author.send(f"```{tabulate(table, tablefmt='presto')}```")
        emojis = ReactionPredicate.NUMBER_EMOJIS[:len(guilds)]

        start_adding_reactions(msg, emojis)
        pred = ReactionPredicate.with_emojis(emojis, msg)
        await bot.wait_for("reaction_add", check=pred)
        await author.send(pred.result)

        guild = guilds[pred.result]
    else:
        #guild = bot.get_guild(554733245187751966)
        guild = guilds[0]

    async with config.user(author).info() as history:
        now = datetime.now()
        try:
            print('[ModMail] Attempting to find {author.name} message frequncy')
            history['counter'] += 1
            history['last_messaged'] = datetime.timestamp(now)
            history['is_waiting'] = True
            history['guild_id'] = guild.id
            print(f"[ModMail] {author.name} message frequency: {history['counter']}")
        except KeyError:
            print('[ModMail] User not found, created a new entry')
            history['counter'] = 1
            history['last_messaged'] = datetime.timestamp(now)
            history['is_waiting'] = True
            history['guild_id'] = guild.id

    modmail_thread = await channel_finder(author, guild)

    if not modmail_thread:
        modmail_thread = await create.new_modmail_thread(bot, guild, author)
        if not modmail_thread:
            return await author.send(
                "Missing permissions from the guild you are trying to send a message to, please speak with owner of said guild.")

    await modmail_thread.send(
        embed = await message_from_user_embed(message, author))
