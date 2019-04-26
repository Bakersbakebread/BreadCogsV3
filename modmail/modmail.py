import discord
from discord.ext import commands

from . import handle_messages, create

import datetime

from redbot.core import Config, checks, commands
from redbot.core.bot import Red


class Modmail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=2807305259608965131)

        default_global = {
            "blocked": []
        }
        self.config.register_global(**default_global)

        default_guild = {
            "help_message_id": None,
            "log_channel_id": None,
        }
        self.config.register_guild(**default_guild)

        default_user = {
            # TODO: Move blocked into here
            "info": {
                "counter": 0,
                "last_messaged": None,
                "guild_id": 0,
                "is_waiting": False,
                "multi_guild_hold": False
            }
        }
        self.config.register_user(**default_user)

    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if isinstance(message.channel, discord.abc.PrivateChannel):
            await handle_messages.message_mods(self.bot, message, self.config)

    @commands.command()
    async def create(self, ctx):
        """Setup a new ModMail"""
        await create.new_modmail(ctx, self.config)

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
            if x.name != 'test':
                await x.delete()

    @commands.command()
    async def test(self, ctx):
        await ctx.send("Spinning up Flask")
        await ctx.send("Flask App Running on localhost:8990")
    ####################
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
            return await ctx.send(':thinking: It\'s not a good idea to block me.')

        user_blocked = await self.is_user_blocked(user, self.config)
        if not user_blocked:
            await self.toggle_blocked(user)
            await ctx.send(f'🛡️ :mute: {user.name} has been blocked.')
        else:
            await ctx.send(f":no_entry: :mute: {user.name} is already blocked.")

    @commands.command()
    async def unblock(self, ctx, user: discord.Member):
        """Block a user from message mod's."""
        if user.id == ctx.me.id:
            await ctx.send(':thinking:')
        blocked = await self.is_user_blocked(user, self.config)
        if blocked:
            await self.toggle_blocked(user)
            await ctx.send(f':loud_sound: {user.name} has been unblocked.')
        else:
            await ctx.send(f":no_entry: {user.name} is not blocked.")
