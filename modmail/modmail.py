import discord
from discord.ext import commands

from . import create
from .handle_messages import *

import datetime
import functools

from redbot.core import Config, checks, commands
from redbot.core.bot import Red

from .utils import *


class Modmail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=2807305259608965131)

        default_global = {"blocked": []}
        self.config.register_global(**default_global)

        default_guild = {
            "help_message_id": None,
            "log_channel_id": None,
            "category_id": None,
        }
        self.config.register_guild(**default_guild)

        default_user = {
            # TODO: Move blocked into here
            "info": {
                "counter": 0,
                "last_messaged": None,
                "guild_id": 0,
                "thread_is_open": False,
                "multi_guild_hold": False,
                "thread_id": 0,
                "current_thread": [],
                "archive": [],
            }
        }
        self.config.register_user(**default_user)

    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if isinstance(message.channel, discord.abc.PrivateChannel):
            await message_mods(self.bot, message, self.config)

    async def is_thread(self, guild, channel_to_check):
        config_category_id = await self.config.guild(guild).category_id()
        if channel_to_check.category is not None:
            if channel_to_check.category.id != config_category_id:
                return False
        else:
            return False
        return True

    @commands.command()
    async def create(self, ctx):
        """Setup a new ModMail"""
        loading = await ctx.send("⏳ Creating new ModMail...")
        await create.new_modmail(ctx, self.config)
        await loading.edit(content="👍 ModMail Created")

    @commands.command()
    # async def aik(self, ctx):
    async def aik(self, ctx, user: discord.Member):
        await create.new_modmail_thread(self.bot, ctx.guild, user)
        channel_check = ctx.guild.channels
        for channel in channel_check:
            if str(ctx.author.id) in channel.name:
                await ctx.send(channel.name)

    @commands.command()
    async def clean(self, ctx):
        for x in ctx.guild.channels:
            if x.name != "test":
                await x.delete()

    ####################
    # replying to user #
    ####################

    @commands.command()
    async def reply(self, ctx, *, quick_message=None):
        # is_thread = await self.is_thread(ctx.guild, ctx.channel)
        # if not is_thread:
        #    return await ctx.send("This is not a thread.")

        # user_id = ctx.channel.topic.split()[5]
        user_id = 280730525960896513
        user = await self.bot.get_user_info(user_id)

        if quick_message:
            message = quick_message
        else:
            service = await reply_service(ctx, user)
            message = service[0]

        embed = discord.Embed(title="Message preview", description=message)

        reply = await ctx.send(embed=embed)

        approved = await yes_or_no(
            ctx, message=f"Would you like to send message to {user.name}?"
        )

        if approved:
            await reply_to_user(ctx, self.config, message, user, is_anon=False)
        else:
            await ctx.send("Ok. Message not sent.", delete_after=30)

        await reply.delete()
        await ctx.message.delete()
        if not quick_message:
            await service[1].delete()

    @commands.command()
    async def replyanon(self, ctx, *, quick_message=None):
        # is_thread = await self.is_thread(ctx.guild, ctx.channel)
        # if not is_thread:
        #    return await ctx.send("This is not a thread.")

        # user_id = ctx.channel.topic.split()[5]
        user_id = 280730525960896513
        user = await self.bot.get_user_info(user_id)
        if quick_message:
            message = quick_message
        else:
            service = await reply_service(ctx, user)
            message = service[0]

        embed = discord.Embed(title="Message preview", description=message)
        embed.set_footer(text=await get_label("info", "sending_anon"))

        reply = await ctx.send(embed=embed)

        approved = await yes_or_no(
            ctx, message=f"Would you like to send message to {user.name}?"
        )

        if approved:
            await reply_to_user(ctx, self.config, message, user, is_anon=True)
        else:
            await ctx.send("Ok. Message not sent.", delete_after=30)

        await reply.delete()
        await ctx.message.delete()
        if not quick_message:
            await service[1].delete()

    #####################
    # closing thread    #
    #####################
    @commands.command()
    async def close(self, ctx, time_delay=None):
        is_thread = await self.is_thread(ctx.guild, ctx.channel)
        if not is_thread:
            return await ctx.send("This is not a thread.")

        approved = await yes_or_no(
            ctx, message="Are you sure you want to close this thread?"
        )
        if not approved:
            await ctx.message.delete()
            return await ctx.send("Okay. Thread will remain open.", delete_after=30)

        loading = await ctx.send(":hourglass: Closing ModMail Thread")

        user_id = ctx.channel.topic.split()[5]
        user = await self.bot.get_user_info(user_id)
        
        async with self.config.user(user).info() as user_info:
            current_thread = {user_info['thread_id'] :user_info['current_thread']}
            
            user_info.update(
                {"thread_is_open": False, 
                 "thread_id": 0,
                 "current_thread": []})

            user_info['archive'].append(current_thread)

        embed = discord.Embed(
            title=f" ",
            description=f"ModMail Thread closed by {ctx.author.name}",
            color=discord.Color.red(),
        )
        await loading.edit(embed=embed, content=f" ")
        approved = await yes_or_no(
            ctx, message="Would you like to delete the channel?"
        )
        if approved:
            await ctx.send("Delete")
        else:
            await ctx.send("dont")

    #####################
    # blocking users   #
    ####################
    @staticmethod
    async def is_user_blocked(user, config):
        """Find out if user is blocked"""
        async with config.blocked() as blocked:
            if user.id in blocked:
                return True
            else:
                return False

    async def toggle_blocked(self, user):
        async with self.config.blocked() as blocked:
            if user.id in blocked:
                blocked.remove(user.id)
            else:
                blocked.append(user.id)

    @commands.command()
    async def block(self, ctx, user: discord.Member):
        """Block a user from message mod's."""
        if user.id == ctx.me.id:
            return await ctx.send(":thinking: It's not a good idea to block me.")

        user_blocked = await self.is_user_blocked(user, self.config)
        if not user_blocked:
            await self.toggle_blocked(user)
            await ctx.send(f":shield: :mute: {user.name} has been blocked.")
        else:
            await ctx.send(f":no_entry: :mute: {user.name} is already blocked.")

    @commands.command()
    async def unblock(self, ctx, user: discord.Member):
        """Block a user from message mod's."""
        if user.id == ctx.me.id:
            await ctx.send(":thinking:")
        blocked = await self.is_user_blocked(user, self.config)
        if blocked:
            await self.toggle_blocked(user)
            await ctx.send(f":loud_sound: {user.name} has been unblocked.")
        else:
            await ctx.send(f":no_entry: {user.name} is not blocked.")
