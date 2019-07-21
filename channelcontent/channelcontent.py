import discord
from redbot.core import Config, commands

from .settings import ChannelContentSettings


class ChannelContent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Config.get_conf(
            self, identifier=591344887128129557, force_registration=True
        )
        self.settings = ChannelContentSettings(self.bot, self.db)

        self.db.register_global(is_enabled=True)

        default_channel = {
            "is_removing": True,
            "is_silent": False,
            "is_text_only": False,
            "is_image_only": False,
            "text_only_message": "`{}` does not allow images",
            "image_only_message": "`{}` only allows images",
        }

        self.db.register_channel(**default_channel)

    async def is_message_image(self, message: discord.Message) -> bool:
        """
        Checks if message is an image
        """
        is_image = False

        has_embeds = len(message.embeds) > 0
        if has_embeds:
            is_image = False if message.embeds[0].type == "rich" else True

        if len(message.attachments) > 0:
            is_image = True
        return is_image

    async def maybe_send_private(
        self, author: discord.Member, channel: discord.TextChannel, message
    ):
        try:
            await author.send(message.format(channel))
        except discord.errors.Forbidden:
            await channel.send(
                "{mention} - {message}".format(
                    mention=author.mention, message=message.format(channel)
                ),
                delete_after=30,
            )

    async def maybe_delete(self, message: discord.Message):
        channel = message.channel
        is_message_image = await self.is_message_image(message)
        is_text_only = await self.db.channel(channel).is_text_only()
        is_image_only = await self.db.channel(channel).is_image_only()
        is_removing = await self.db.channel(message.channel).is_removing()
        is_silent = await self.db.channel(message.channel).is_silent()

        if not is_removing:
            return

        if not any([is_image_only, is_text_only]):
            return

        if is_image_only and not is_message_image:
            try:
                await message.delete()
                remove_message = await self.db.channel(
                    message.channel
                ).image_only_message()
            except discord.errors.Forbidden:
                return await channel.send(
                    f"Could not delete message, missing `manage_messages` permission."
                )

        elif is_text_only and is_message_image:
            try:
                await message.delete()
                remove_message = await self.db.channel(
                    message.channel
                ).text_only_message()
            except discord.errors.Forbidden:
                return await channel.send(
                    f"Could not delete message, missing `manage_messages` permission."
                )
        else:
            return

        if not is_silent:
            await self.maybe_send_private(message.author, channel, remove_message)

    @commands.Cog.listener(name="on_message")
    async def _check_message_content(self, message: discord.Message):
        """
        Message handler to check message content and remove if necessary
        """
        if not await self.db.is_enabled():
            return

        if (message.author == self.bot.user) or (
            isinstance(message.channel, discord.abc.PrivateChannel)
        ):
            return

        await self.maybe_delete(message)

    @commands.group(name="chcontent")
    async def _channel_content(self, ctx):
        """Lock down your channel to be image, or text only"""
        pass

    @_channel_content.command(name="toggle")
    async def _toggle_enabled(self, ctx):
        """
        Globally toggle on/off filtering channel content

        Example: `[p]chcontent toggle`
        """
        prev, new = await self.settings.toggle_is_enabled()

        return await ctx.send(f"Toggled channel content filtering from `{prev}` to `{new}`.")

    @_channel_content.command(name="silent")
    async def _toggle_silent_remove(self, ctx, channel: discord.TextChannel = None):
        """
        Toggle removing messages silently

        This defaults to the channel the command is ran in, but accepts a channel argument.

        If silent is set to False, the user will receive a message when their prohibited message
        is deleted.

        Example: `[p]chcontent silent  600655665975001098`
        """
        if channel is None:
            channel = ctx.channel

        prev, new = await self.settings.toggle_silent_remove(channel)

        return await ctx.send(f"Toggled silently removing messages from `{prev}` to `{new}` in `{channel}`.")

    @_channel_content.command(name="text")
    async def _set_text_only(self, ctx, channel=None):
        """
        Set the channel to be text only


        Example: `[p]chcontent text 591344887128129557`
        """
        if channel is None:
            channel = ctx.channel

        await self.settings.set_text_only(channel)

        await ctx.send(f"{channel} is now text only.")
        is_text_only = await self.db.channel(channel).is_text_only()
        await ctx.send(f"Debug {is_text_only}")

    @_channel_content.command(name="image", aliases=["img", "images"])
    async def _set_image_only(self, ctx, channel=None):
        """
        Set the channel to be image only


        example: `[p]chcontent image 591344887128129557`
        """
        if channel is None:
            channel = ctx.channel

        await self.settings.set_image_only(channel)

        await ctx.send(f"{channel} is now image only.")
        is_text_only = await self.db.channel(channel).is_image_only()
        await ctx.send(f"Debug {is_text_only}")

    @_channel_content.group(name="message")
    async def _set_error_messages(self, ctx):
        """
        Set the error messages for the current channel
        """
        pass

    @_set_error_messages.command(name="text")
    async def _set_text_only_message(self, ctx, *, message):
        """
        Set the error message a user receives when a message is deleted in this channel.

        To use the channel name within your message please add {}.

        Example: [p]chcontent message text {} only allows text messages.
        """

        prev, new = await self.settings.set_text_only_message(channel=ctx.channel, new_message=message)

        await ctx.send(
            "**Changed text only message from:**\n```{prev}```**To:**\n```{new}``` ".format(
                prev=prev.format(ctx.channel),
                new=new.format(ctx.channel)
            ))

    @_set_error_messages.command(name="image")
    async def _set_image_only_message(self, ctx, *, message):
        """
        Set the error message a user receives when a message is deleted in this channel.

        To use the channel name within your message please add {}.

        Example: [p]chcontent message text {} only allows text messages.
        """

        prev, new = await self.settings.set_image_only_message(channel=ctx.channel, new_message=message)

        await ctx.send(
            "**Changed text only message from:**\n```{prev}```**To:**\n```{new}``` ".format(
                prev=prev.format(ctx.channel),
                new=new.format(ctx.channel)
            ))