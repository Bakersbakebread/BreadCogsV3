import json
import logging
import aiohttp
import discord

from redbot.core import Config, checks
from redbot.core.commands import commands

log = logging.getLogger(name="red.breadcogs.baddomains")

DEFAULT_GUILD_CONFIG = {
    "log_channel": None,
    "should_delete": False,
}

DOMAIN_LIST_URL = "https://bad-domains.walshy.dev/domains.json"


class BadDomains(commands.Cog):
    """Checks against a list of bad domains and reports it so.

    The full list is here: https://github.com/WalshyDev/Discord-bad-domains"""

    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.config = Config.get_conf(self, identifier=280730525960896513)
        self.config.register_guild(**DEFAULT_GUILD_CONFIG)
        self.domain_list = None

    @checks.admin_or_permissions(manage_guild=True)
    @commands.group(name="baddomains", aliases=["bd"])
    async def baddomains_group(self, ctx):
        pass

    @baddomains_group.command(name="log")
    async def log_command(self, ctx, channel: discord.TextChannel = None):
        """Set the log channel

        Passing no channel will disable logging by removing the channel.
        """
        if channel is None:
            await self.config.guild(ctx.guild).log_channel.set(None)
            return await ctx.send("I've removed the log channel, this has disabled log messages.")

        await self.config.guild(ctx.guild).log_channel.set(channel.id)
        return await ctx.send(f"👍 I will send log messages to {channel}.")

    @baddomains_group.command(name="delete")
    async def delete_command(self, ctx, should_delete: bool):
        """
        Set whether or not to delete a message when found.

        should_delete takes in bools: `True` or `False`
        """
        await self.config.guild(ctx.guild).should_delete.set(should_delete)
        return await ctx.send(
            f"I will {'delete messages' if should_delete else 'not do aything'}, when a bad domain is found."
        )

    @baddomains_group.command(name="settings")
    async def settings_command(self, ctx):
        """
        Show current settings.
        """
        should_delete = await self.config.guild(ctx.guild).should_delete()
        log_channel = await self.config.guild(ctx.guild).log_channel()

        if log_channel:
            tm = ctx.guild.get_channel(log_channel)
            if isinstance(tm, discord.TextChannel):
                log_channel = tm

        embed = discord.Embed(title="Bad domains settings")
        embed.add_field(name="Deleting messages", value=should_delete, inline=False)
        channel_value = f"{log_channel.mention} - `{log_channel.id}`" if log_channel else "None set (disabled)"
        embed.add_field(name="Log Channel", value=channel_value, inline=False)

        await ctx.send(embed=embed)

    @commands.Cog.listener(name="on_message_without_command")
    async def on_message_listener(self, message: discord.Message):
        """Handles the messages incoming, transforms them and sends them for evaulation."""
        if message.author.bot:
            return

        if not message.guild:
            return

        if await self.bot.is_automod_immune(message.author):
            return

        content = message.clean_content.lower()

        try:
            contains_bad_domain = await self.contains_bad_domain(content)
            if contains_bad_domain:
                await self.handle_bad_domain(message)
        except RuntimeError as e:
            # lets just fail silently.
            log.exception(e)
            return

    async def contains_bad_domain(self, clean_content):
        if self.domain_list is None:
            await self.populate_domain_list()

        for domain in self.domain_list:
            if domain in clean_content:
                return True

    async def populate_domain_list(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=DOMAIN_LIST_URL) as resp:
                if resp.status == 200:
                    resp_json = await resp.json()
                    self.domain_list = resp_json
                else:
                    raise RuntimeError("Api returned bad status.")

    async def handle_bad_domain(self, message):
        should_delete = await self.config.guild(message.guild).should_delete()
        log_channel = await self.config.guild(message.guild).log_channel()

        if should_delete:
            try:
                await message.delete()
            except discord.errors.Forbidden:
                pass

        if log_channel is not None:
            embed = discord.Embed(title="Bad domain detected")
            embed.set_author(
                name=f"{message.author} - {message.author.id}",
                icon_url=message.author.avatar_url
            )
            embed.add_field(
                inline=False,
                name="Message",
                value=f"{message.clean_content}\n\n"
                      f"\N{LINK SYMBOL} [Jump to message]({message.jump_url})"
            )
            await message.guild.get_channel(log_channel).send(embed=embed)
