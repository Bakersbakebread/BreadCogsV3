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
    async def reply(self, ctx, is_anon=False):
        # is_thread = await self.is_thread(ctx.guild, ctx.channel)
        # if not is_thread:
        #    return await ctx.send("This is not a thread.")

        # user_id = ctx.channel.topic.split()[5]
        user_id = 280730525960896513
        user = await self.bot.get_user_info(user_id)

        anon = "`Sending anonymously`" if is_anon else f" "
        ask_for_message = await ctx.send(f"What is your reply? {anon}")

        def check(m):
            return user.id == m.author.id

        message = await ctx.bot.wait_for("message", check=check)

        await message.delete()
        embed = discord.Embed(title="Message preview", description=message.content)

        if is_anon:
            embed.set_footer(text="Sending message anonymously")
        reply = await ctx.send(embed=embed)

        approved = await yes_or_no(ctx, user)

        if approved:
            await reply_to_user(ctx, message, user, is_anon)
        else:
            await ctx.send("Ok. Message not sent.", delete_after=30)

        await reply.delete()
        await ctx.message.delete()
        await ask_for_message.delete()

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
