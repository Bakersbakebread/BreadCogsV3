import logging
import re
import discord
from dislash import ActionRow, Button, ButtonStyle

from redbot.core import Config, checks
from redbot.core.commands import commands
from .api import Api, CheckEndpointResponseModel

log = logging.getLogger(name="red.breadcogs.baddomains")

DEFAULT_GUILD_CONFIG = {
    "log_channel": None,
    "report_channel": None,
    "should_delete": False,
    "should_kick": False,
    "should_ban": False,
}

CUSTOM_ID_PREFIX = "badDomainBtn"


def get_list_of_links_from_message(message: str) -> [str]:
    return re.findall(r'(https?://[^\s]+)', message.lower())


class BadDomains(commands.Cog):
    """Checks against a list of bad domains and reports it so.

    The full list is here: https://github.com/WalshyDev/Discord-bad-domains"""

    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.config = Config.get_conf(self, identifier=280730525960896513)
        self.config.register_guild(**DEFAULT_GUILD_CONFIG)
        self.api = Api()

    def cog_unload(self):
        """
        Teardown the slash client so we don't have multiple clients
        """
        self.bot.slash.teardown()

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

    @baddomains_group.command(name="kick")
    async def kick_command(self, ctx, should_kick: bool):
        """
        Set whether or not to delete a message when found.

        should_delete takes in bools: `True` or `False`
        """
        await self.config.guild(ctx.guild).should_kick.set(should_kick)
        return await ctx.send(
            f"I will {'kick the user' if should_kick else 'not kick'}, when a bad domain is found."
        )

    @baddomains_group.command(name="ban")
    async def ban_command(self, ctx, should_ban: bool):
        """
        Set whether or not to delete a message when found.

        should_delete takes in bools: `True` or `False`
        """
        await self.config.guild(ctx.guild).should_ban.set(should_ban)
        return await ctx.send(
            f"I will {'ban the user' if should_ban else 'not ban'}, when a bad domain is found."
        )

    @baddomains_group.command(name="report")
    async def report_channel(self, ctx, channel: discord.TextChannel = None):
        """
        Set whether or not to delete a message when found.

        should_delete takes in bools: `True` or `False`
        """
        if channel is None:
            await self.config.guild(ctx.guild).report_channel.set(None)
            return await ctx.send("I've removed the report channel, this has disabled report messages.")

        await self.config.guild(ctx.guild).report_channel.set(channel.id)
        return await ctx.send(f"👍 I will send report messages to {channel}.")

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

        list_of_links = get_list_of_links_from_message(message.clean_content)

        if not list_of_links:
            return

        log.debug(list_of_links)

        try:
            for domain in list_of_links:
                response = await self.api.check(domain)
                if response.bad_domain:
                    log.info(f"Bad domain found: {domain}")
                    await self.handle_bad_domain(message, response, domain)

        except RuntimeError as e:
            # lets just fail silently.
            log.exception(e)
            return

    async def handle_bad_domain(self, message: discord.Message, response, domain):
        should_delete = await self.config.guild(message.guild).should_delete()
        should_ban = await self.config.guild(message.guild).should_ban()
        should_kick = await self.config.guild(message.guild).should_kick()
        log_channel = await self.config.guild(message.guild).log_channel()

        action_reason = "[AutoMod] [BadDomain] - bad link detected"

        message_deleted = False
        if should_delete:
            try:
                await message.delete()
                message_deleted = True
                log.info(f"Deleted message with bad domain: {domain}")
            except discord.errors.Forbidden or discord.errors.NotFound as e:
                log.warning(f"Could not delete message with bad domain: {domain} - {e.args[0]}")
                pass

        guild: discord.Guild = message.guild

        user_banned = False
        if should_ban:
            try:
                await guild.ban(message.author, delete_message_days=1, reason=action_reason)
                log.info(f"Banned user for bad domain, {domain}")
                user_banned = True
            except discord.errors.Forbidden as e:
                log.info(f"missing permissions to ban {message.author} - {e.args[0]}")
                pass

        user_kicked = False
        if should_kick:
            try:
                await guild.kick(message.author, reason=action_reason)
                user_kicked = True
                log.info(f"Kicked user for bad domain, {domain}")
            except discord.errors.Forbidden or discord.errors.NotFound as e:
                log.info(f"Failed to kick {message.author} - {e.args[0]}")
                pass

        if log_channel is None:
            log.warning("No log set, failed to send message.")
            return

        embed = discord.Embed(title="Bad domain detected")
        embed.set_author(
            name=f"{message.author} - {message.author.id}",
            icon_url=message.author.avatar_url
        )
        embed.add_field(
            inline=False,
            name="Message",
            value=f"{message.clean_content}\n\n"
        )
        embed.add_field(
            inline=False,
            name="Bad domain",
            value=domain
        )
        if message_deleted:
            embed.add_field(name="🗑 Message deleted",
                            value=f"The message has been removed")

        if not message_deleted:
            embed.add_field(name="\N{LINK SYMBOL} Message not deleted",
                            value=f"[Jump to message]({message.jump_url})")

        if user_banned:
            embed.add_field(name="Action taken", value=f"{message.author} has been banned.")

        if user_kicked:
            embed.add_field(name="Action taken", value=f"{message.author} has been kicked.")

        channel = message.guild.get_channel(log_channel)
        await channel.send(embed=embed)
        log.info(f"Sent bad domain log to {channel}")

    @baddomains_group.command(name="submit")
    async def handle_reporting(self, ctx, *, message):

        links = get_list_of_links_from_message(message)

        if not links:
            return await ctx.send("Mmm. I couldn't find any links in that message.")

        btn = Button(
            label="Report bad domain",
            emoji=discord.PartialEmoji(name="👮"),
            custom_id=f"{CUSTOM_ID_PREFIX}:{links[0]}",
            style=ButtonStyle.primary)

        row = ActionRow(btn)

        embed = discord.Embed(
            title="Thanks for your report",
            description="To report this link as a bad domain, click the button below.")

        embed.add_field(name="Bad domain found", value=links[0])

        await ctx.send(embed=embed, components=[row])

    @commands.Cog.listener()
    async def on_button_click(self, inter):
        button_id = inter.component.custom_id
        if not button_id.startswith(CUSTOM_ID_PREFIX):
            return

        bad_domain = button_id.replace(CUSTOM_ID_PREFIX, "")

        await self.api.report(bad_domain)

        updated_embed = inter.message.embeds[0]
        updated_embed.add_field(
            inline=False,
            name="Reported as bad",
            value=f"{inter.author} marked this as a bad domain. Updating the list can take some time."
        )
        updated_embed.color = discord.Color.dark_green()
        await inter.message.edit(embed=updated_embed, components=[])

        await inter.reply(f"🙌 Thanks. I've reported this domain as being bad.", delete_after=5, ephemeral=True)
