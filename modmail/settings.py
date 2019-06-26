import discord
from .exceptions import AlertsChannelExists, InvalidPortRange
from datetime import datetime
from tabulate import tabulate

EMPTY = "⠀"

class ModMailSettings:
    def __init__(self, bot: discord.Client, context, config):
        self.bot = bot
        self.ctx = context
        self.config = config

    async def get_all_settings(self) -> discord.Embed:
        guild = self.ctx.guild
        settings = []

        def true_or_false(value):
            return ("`Enabled`" if value else "`Disabled`")

        guild_group = await self.config.guild(guild).all()
        all_group = await self.config.all()

        alerts_channel = self.bot.get_channel(guild_group.get('modmail_alerts_channel', 'None'))
        enforced_guild = all_group.get('enforced_guild', None)
        enforced_guild = ("`Disabled`" if not enforced_guild else self.bot.get_guild(enforced_guild))

        discord_settings = (
            f":bell: Alerts: {true_or_false(guild_group['modmail_alerts'])}\n"
            f":newspaper: Alert channel: <#{alerts_channel.id}>\n"
            f":shield: Enforcing single guild: `{enforced_guild}`\n"
            f":scissors: Available snippets: `{len(guild_group['snippets'])}`"
        )
        web_settings = (
            f":desktop: Port number: `{all_group.get('port')}`\n"
            f":mouse_three_button: Redirect URI: http://20.73.53.123/callback\n\n"
        )

        embed = discord.Embed(title="ModMail Settings")
        embed.add_field(name="Discord settings", value=discord_settings, inline=True)
        embed.add_field(name="Web settings", value=web_settings, inline=True)


        return embed

    async def get_guild_snippets(self, guild: discord.TextChannel):
        all_snippets = await self.config.guild(guild).snippets()
        return all_snippets

    async def add_new_snippet(self, guild, code, snippet):
        guild_group = self.config.guild(guild)

        snippet_dict = {
            "author": self.ctx.author.id,
            "created_at": self.ctx.message.created_at.strftime("%m/%d/%Y, %H:%M"),
            "content": snippet,
            "code": code
        }

        async with guild_group.snippets() as snippets:
            snippets.append(snippet_dict)

    async def set_channel(self, channel: discord.TextChannel) -> tuple:
        guild = self.ctx.guild
        before_id = await self.config.guild(guild).modmail_alerts_channel()

        if before_id == channel.id:
            raise AlertsChannelExists
        before = self.bot.get_channel(before_id)

        await self.config.guild(guild).modmail_alerts_channel.set(channel.id)
        after = self.bot.get_channel(channel.id)

        return ((before if before else None), after)

    async def set_alerts(self) -> bool:
        guild = self.ctx.guild

        before = await self.config.guild(guild).modmail_alerts()
        await self.config.guild(guild).modmail_alerts.set(not before)

        return not before

    async def set_port(self, port: int) -> tuple:
        port_in_config = await self.config.port()
        accepted_range = range(1, 65535)

        if port not in accepted_range:
            raise InvalidPortRange

        await self.config.port.set(port)

        return port_in_config, port

    async def set_enforced_guild(self, guild) -> tuple:
        guild_in_config = await self.config.enforced_guild()
        if guild is None:
            await self.config.enforced_guild.set(None)
            return (None, guild_in_config)

        await self.config.enforced_guild.set(int(guild))

        after_id = await self.config.enforced_guild()
        after = self.bot.get_guild(after_id)

        return (guild_in_config, after)
