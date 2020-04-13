import discord

from redbot.core.commands import commands


class AutoReactListeners:
    def __init__(self, config):
        self.config = config

    @staticmethod
    async def add_reactions(target: discord.Message, emojis):
        for emoji in emojis:
            try:
                await target.add_reaction(emoji)
            except discord.errors.Forbidden:
                pass # the message may have been quickly deleted or such

    @commands.Cog.listener()
    async def on_message_without_command(self, message: discord.Message):
        channel_emojis = await self.config.channel(message.channel).emojis()
        member_emojis = await self.config.member(message.author).emojis()
        ignore_bots = await self.config.channel(message.channel).ignore_bots()

        if ignore_bots is True and message.author.bot:
            return

        if channel_emojis:
            await self.add_reactions(message, channel_emojis)

        if member_emojis:
            await self.add_reactions(message, member_emojis)
