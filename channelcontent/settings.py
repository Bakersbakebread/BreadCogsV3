import discord


class ChannelContentSettings:
    def __init__(self, bot, config):
        self.bot = bot
        self.db = config

    async def toggle_is_enabled(self):
        """Enables / disabled channel content globally"""
        previous_setting = await self.db.is_enabled()
        new_setting = not previous_setting
        await self.db.is_enabled.set(new_setting)

        return previous_setting, new_setting

    async def toggle_silent_remove(self, channel: discord.TextChannel) -> tuple:
        """Toggles whether the bot will message user when removing a message"""
        previous_setting = await self.db.channel(channel).is_silent()
        new_setting = not previous_setting
        await self.db.channel(channel).is_silent.set(new_setting)

        return previous_setting, new_setting

    async def set_text_only(self, channel: discord.TextChannel) -> None:
        """Sets channel provided to text only"""
        await self.db.channel(channel).is_text_only.set(True)
        await self.db.channel(channel).is_image_only.set(False)

    async def set_image_only(self, channel: discord.TextChannel) -> None:
        """Sets channel provided to image only"""
        await self.db.channel(channel).is_text_only.set(False)
        await self.db.channel(channel).is_image_only.set(True)

    async def set_text_only_message(
        self, channel: discord.TextChannel, new_message: str
    ):
        """Set the text-only message sent to users"""
        previous_message = await self.db.channel(channel).text_only_message()
        await self.db.channel(channel).text_only_message.set(new_message)

        return previous_message, new_message

    async def set_image_only_message(
        self, channel: discord.TextChannel, new_message: str
    ):
        """Set the image-only message sent to users"""
        previous_message = await self.db.channel(channel).image_only_message()
        await self.db.channel(channel).image_only_message.set(new_message)

        return previous_message, new_message
