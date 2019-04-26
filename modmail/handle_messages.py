import discord

from redbot.core import Config, checks, commands
from redbot.core.bot import Red

from . import create


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
    message_from_user.set_footer(text=f"Sent : 15:00 20th Feb 2019")

    return message_from_user

async def channel_finder(author, guild):
    for channel in guild.channels:
        if str(author.id) in channel.name:
            return channel

async def message_mods(bot, message, config):
    author = message.author
    # # channel_name = discord.utils.get(self.bot.guilds, id=556800157082058784)

    # Get a list of guilds the user & bot share
    guilds = [member.guild for member in bot.get_all_members()
              if member.id == author.id]

    # if len(guilds) > 1:
    #   return await author.send('We have too many guilds in common.')

    # guild = guilds[0]
    # print(guild)

    guild = bot.get_guild(554733245187751966)

    async with config.user(author).info() as history:
        await author.send(history)
        try:
            history['counter'] += 1
            print('Attempting to find user frequncy')
            print(f"[ModMail] User frequency for {author.name} : {history[str(author.id)]}")
        except KeyError:
            print('User not found, created a new entry')
            history['counter'] = 1

    modmail_thread = await channel_finder(author, guild)

    if not modmail_thread:
        modmail_thread = await create.new_modmail_thread(bot, guild, author)

    await modmail_thread.send(
        embed = await message_from_user_embed(message, author))
