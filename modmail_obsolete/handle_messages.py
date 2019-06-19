import discord
import json
import os
from datetime import datetime

from .create import thread
from .utils import *

from redbot.core import Config, checks, commands
from redbot.core.bot import Red

from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.data_manager import cog_data_path

from redbot.core.utils.chat_formatting import inline

from tabulate import tabulate


async def please_wait_reply(author):
    # message = "Your message has been recieved.  Someone will reply as soon as
    # possible."

    message = await get_label("info", "guild_react_request")
    # message = label.get("help_message", "Thanks for helping")
    await author.send(message)


async def message_embed(message, author, is_mod=True, is_anon=True, is_not_reply=True):
    # TODO: Handle attachments
    # TODO: Make colors custom
    color = discord.Color.green() if is_mod else discord.Color.orange()

    embed = discord.Embed(description=(f"{message}"), color=color)

    embed.set_author(
        name=(f" " if is_anon else f"{author.name}"), icon_url=f"{author.avatar_url}"
    )

    if is_not_reply:
        salutation = "Mod" if is_mod else "User"
    else:
        salutation = "Click here to view more"
    embed.set_footer(text=f"{salutation}")

    return embed


async def channel_finder(author, guild):
    for channel in guild.channels:
        if str(author.id) in channel.name:
            return channel


async def reply_service(ctx, user):
    ask_for_message = await ctx.send("What is your reply?")

    def check(m):
        return user.id == m.author.id

    message_obj = await ctx.bot.wait_for("message", check=check)
    message = message_obj.content
    await message_obj.delete()

    return (message, ask_for_message)


async def reply_to_user(ctx, config, message, user, is_anon):
    try:
        await user.send(inline(await get_label("info", "user_modmail_recieved")))
        await user.send(
            embed=await message_embed(
                message, ctx.author, is_anon=is_anon, is_not_reply=False
            )
        )
        embed = await message_embed(message, user, is_anon=False)
        if is_anon:
            embed.set_footer(text="Mod | Sent Anonymously")
        await ctx.send(embed=embed)
        await save_message_to_config(config, user, embed)
    except discord.errors.Forbidden:
        await ctx.send(await get_label("errors", "dm_not_allowed"))



