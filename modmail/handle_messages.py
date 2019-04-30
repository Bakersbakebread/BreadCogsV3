import discord
import json
import os
from datetime import datetime

from redbot.core import Config, checks, commands
from redbot.core.bot import Red

from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.data_manager import cog_data_path

from . import create

from modmail import modmail
from tabulate import tabulate


with open(
    os.path.join(cog_data_path(raw_name="ModMail"), "dictionary.json")
) as json_file:
    data = json.load(json_file)


async def please_wait_reply(author):
    # message = "Your message has been recieved.  Someone will reply as soon as
    # possible."

    message = data.get("help_message", "Thanks for helping")
    await author.send(message)


async def message_embed(message, author, is_mod=False):
    # TODO: Handle attachments
    # TODO: Make colors custom
    color = discord.Color.green() if is_mod else discord.Color.orange()

    embed = discord.Embed(description=(f"{message.content}"), color=color)

    embed.set_author(name=f"{author.name}", icon_url=f"{author.avatar_url}")

    salutation = "Mod" if is_mod else "User"
    embed.set_footer(text=f"{salutation}")

    return embed


async def channel_finder(author, guild):
    for channel in guild.channels:
        if str(author.id) in channel.name:
            return channel


async def reply_to_user(ctx, message, user):
    try:
        await user.send(message.content)
        await ctx.send(embed=await message_embed(message, user, True))
    except discord.errors.Forbidden:
        await ctx.send("Unable to send DM to user.")


async def message_mods(bot, message, config):
    author = message.author
    user_info = await config.user(author).info()

    if user_info["multi_guild_hold"]:
        await author.send(
            "Please react with the emoji corresponding to the guild you wish to send to."
        )
        return

    if user_info["thread_is_open"]:
        open_thread = bot.get_channel(user_info["thread_id"])
        if open_thread:
            await open_thread.send(embed=await message_embed(message, author))
            return await message.add_reaction("✅")

    user_is_blocked = await modmail.Modmail.is_user_blocked(author, config)
    if user_is_blocked:
        print(f"[ModMail] Blocked user attempted to message : {author.name}")
        return await author.send(
            "You are have been blocked from sending ModMail messages."
        )

    # # channel_name = discord.utils.get(self.bot.guilds,
    # id=556800157082058784)

    # Get a list of guilds the user & bot share
    guilds = [
        member.guild for member in bot.get_all_members() if member.id == author.id
    ]

    if len(guilds) > 1:
        async with config.user(author).info() as info:
            info["multi_guild_hold"] = True

        table = [[index, guild.name] for index, guild in enumerate(guilds)]

        await author.send(
            "We have more than one server in common, please choose from list below where you would like to send the message."
        )
        msg = await author.send(f"```{tabulate(table, tablefmt='presto')}```")

        emojis = ReactionPredicate.NUMBER_EMOJIS[: len(guilds)]

        start_adding_reactions(msg, emojis)

        pred = ReactionPredicate.with_emojis(emojis, msg)

        await bot.wait_for("reaction_add", check=pred)

        guild = guilds[pred.result]
        await author.send(guild)

    else:
        # guild = bot.get_guild(554733245187751966)
        guild = guilds[0]

    async with config.user(author).info() as user_info:
        # set waiting to True (reset it on reply)
        now = datetime.now()
        try:
            print(f"[ModMail] Attempting to find {author.name} message frequncy")
            user_info["counter"] += 1
            user_info["last_messaged"] = datetime.timestamp(now)
            user_info["thread_is_open"] = True
            user_info["guild_id"] = guild.id
            user_info["multi_guild_hold"] = False
            print(f"[ModMail] {author.name} message frequency: {user_info['counter']}")
        except KeyError:
            print("[ModMail] User not found, created a new entry")
            user_info["counter"] = 1
            user_info["last_messaged"] = datetime.timestamp(now)
            user_info["thread_is_open"] = True
            user_info["guild_id"] = guild.id
            user_info["multi_guild_hold"] = False

    modmail_thread = await channel_finder(author, guild)
    if not modmail_thread:
        # returns False if no permissions to create thread
        modmail_thread = await create.new_modmail_thread(bot, guild, author)
        if not modmail_thread:
            return await author.send(":shield: Missing permissions from that guild.")

    await please_wait_reply(author)
    async with config.user(author).info() as user_info:
        user_info["thread_id"] = modmail_thread.id

    await modmail_thread.send(embed=await message_embed(message, author))
