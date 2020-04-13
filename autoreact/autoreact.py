import discord

from typing import Union, Optional
from discord.ext.commands import Greedy
from redbot.core import Config, checks
from redbot.core.commands import commands

from .listeners import AutoReactListeners
from .utils import yes_or_no


class EmoijiValidationException(Exception):
    def __init__(self, message, emojis):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        # Now for our custom errors
        self.emojis = "\n".join("• `{0}`".format(str(emoji)) for emoji in emojis)


class DontOverrideException(Exception):
    pass


DEFAULT = {"emojis": [], "ignore_bots": True}


class AutoReact(AutoReactListeners, commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=280730525960896513)
        self.config.register_channel(**DEFAULT)
        self.config.register_member(**DEFAULT)
        self.config.register_guild(**DEFAULT)
        self.cache = {"channel": {}, "user": {}}
        super().__init__(self.config, *args, **kwargs)

    @staticmethod
    async def check_emojis_for_inavlid(
        message: discord.Message, emojis: Union[discord.PartialEmoji, discord.Emoji, str]
    ):
        """
        Helper method for analysing any non-conforming emojis
        Parameters
        ----------
        message
            The ctx.message to add reactions to test
        emojis
            The emojis that are to be tested
        Returns
        -------
            List of non-conforming emojis or empty list
        """
        failed_emojis = []
        for emoji in emojis:
            try:
                await message.add_reaction(emoji)
            except discord.errors.HTTPException as e:
                if e.code == 10014:
                    failed_emojis.append(emoji)
        if len(failed_emojis) > 0:
            raise EmoijiValidationException(
                f"> \❌ Invalid emoji{'s' if len(failed_emojis) > 1 else ''} detected",
                failed_emojis,
            )

    async def confirm_override(self, ctx, emojis: Union[discord.PartialEmoji, discord.Emoji, str]):
        """
        Helper method to confirm that user wishes to override already set values for emojis
        Parameters
        ----------
        emojis
            The emojis that will be overridden
        Returns
        -------
            Yes or No bool value
        """
        if not len(emojis) >= 1:
            return
        message = f"There is already a value set. Would you like to override these emojis?\n{', '.join(emojis)}"
        override = await yes_or_no(ctx, message)
        if not override:
            raise DontOverrideException()

    @commands.group(name="autoreact", aliases=["ar"])
    @checks.mod_or_permissions(manage_messages=True)
    async def autoreact_group(self, ctx):
        """
        Auto react to messages, by channel or by member.
        """
        pass

    @autoreact_group.command(name="channel", aliases=["ch", "chan"])
    @checks.mod_or_permissions(manage_messages=True)
    async def _channel_reactions(
        self,
        ctx,
        channel: discord.TextChannel,
        ignore_bots: Optional[bool] ,
        emojis: Greedy[Union[discord.PartialEmoji, discord.Emoji, str]]
    ):
        """Channel-specific reactions
        ```ini
        [channel]
        The channel where reactions will be added```
        ```ini
        [ignore_bots]
        Boolean to set ignoring bots, this is False by default.```
        ```ini
        [emojis]
        The emojis add to the message```
        """
        try:
            # EAFFP
            await self.check_emojis_for_inavlid(ctx.message, emojis)
            await self.confirm_override(ctx, await self.config.channel(channel).emojis())
            sanitised_emojis = [str(emoji) for emoji in emojis]
            await self.config.channel(ctx.channel).emojis.set(sanitised_emojis)
            if ignore_bots:
                await self.config.channel(ctx.channel).ignore_bots.set(ignore_bots)
            if emojis:
                return await ctx.send(
                f"{' '.join(sanitised_emojis)} will be added to every message in {channel.mention}."
            )
            else:
                return await ctx.send(
                    f"🧹 Reactions will not be added in {channel.mention}"
                )
        except DontOverrideException:
            # User does not want to override existing reactions
            return await ctx.send(f"👍 Okay. Nothing's changed.")
        except EmoijiValidationException as e:
            # An emoji is not valid, could be custom or a grouped emoji
            return await ctx.send(f"**{e.args[0]}**{e.emojis}")
        except discord.errors.Forbidden:
            return await ctx.send("Missing permissions to add reactions.")

    @autoreact_group.command(name="member")
    @checks.mod_or_permissions(manage_messages=True)
    async def _member_reactions(
            self,
            ctx,
            member: Union[discord.Member, discord.User],
            emojis: Greedy[Union[discord.PartialEmoji, discord.Emoji, str]]
    ):
        """Member-specific reactions

        ```ini
        [member]
        The discord.Member or discord.User where reactions will be added```
        ```ini
        [emojis]
        The emojis add to the message```
        """
        try:
            # EAFFP
            await self.check_emojis_for_inavlid(ctx.message, emojis)
            await self.confirm_override(ctx, await self.config.member(member).emojis())
            sanitised_emojis = [str(emoji) for emoji in emojis]
            await self.config.member(member).emojis.set(sanitised_emojis)
            if emojis:
                return await ctx.send(
                f"{' '.join(sanitised_emojis)} will be added to every message posted by `{member}` - `{member.id}`."
            )
            else:
                return await ctx.send(
                    f"🧹 Reactions will not be added to any messages by `{member}`"
                )
        except DontOverrideException:
            # User does not want to override existing reactions
            return await ctx.send(f"👍 Okay. Nothing's changed.")
        except EmoijiValidationException as e:
            # An emoji is not valid, could be custom or a grouped emoji
            return await ctx.send(f"**{e.args[0]}**{e.emojis}")
        except discord.errors.Forbidden:
            return await ctx.send("Missing permissions to add reactions.")
