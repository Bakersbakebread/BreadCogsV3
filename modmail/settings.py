import discord
from .exceptions import AlertsChannelExists


class ModMailSettings:
    def __init__(self, bot: discord.Client, context, config):
        self.bot = bot
        self.ctx = context
        self.config = config

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

    async def set_enforced_guild(self, guild) -> tuple:
        guild_in_config = await self.config.enforced_guild()
        if guild is None:
            await self.config.enforced_guild.set(None)
            return (None, guild_in_config)

        await self.config.enforced_guild.set(int(guild))

        after_id = await self.config.enforced_guild()
        after = self.bot.get_guild(after_id)

        return (guild_in_config, after)

