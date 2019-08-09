import discord

import logging
from datetime import datetime

from .exceptions import *
from .settings import R6StatsSettings
from .api import GetApi
from .assets.ranks import NAMES
from .stats_embeds import StatsEmbed

from redbot.core import Config, commands
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.chat_formatting import error
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from redbot.core.checks import is_owner


class R6Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=41398865, force_registration=True
        )
        self.config.register_user(
            username=None,
            platform=None,
            ubisoft_id=None,
            emea_rank=None,
            ncsa_rank=None,
            apac_rank=None,
        )
        self.config.register_global(apikey=None)
        self.settings = R6StatsSettings(self.bot, self.config)

    async def yes_or_no(self, ctx, message):
        msg = await ctx.send(message)
        start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)

        pred = ReactionPredicate.yes_or_no(msg, ctx.author)
        await ctx.bot.wait_for("reaction_add", check=pred)
        await msg.delete()
        return pred.result

    @commands.group(name='r6s', aliases=['R6S', 'r6', 'R6', 'R6s'])
    async def _r6s(self, ctx):
        pass

    @_r6s.command()
    async def profile(self, ctx, username, platform):
        """
        Create your profile to store your username/platform

        Examples:
            `[p]r6s profile bread pc`

        Platform must be one of the following: `pc`, `xbox`, `ps4`.
        """
        author = ctx.author
        conf_username, conf_platform = await self.settings.get_username_platform(author)

        if conf_username or conf_platform is not None:
            override = await self.yes_or_no(
                ctx,
                "You have already set your username and platform. Would you like to override?",
            )
            if not override:
                return await ctx.send(
                    f"Okay. Keeping the following details:"
                    f"\nUsername: `{conf_username}`"
                    f"\nPlatform: `{conf_platform}`"
                )

        try:
            is_player = await GetApi(
                self.bot, self.config, username, platform
            ).is_player(author)
        except NoApiKey:
            return await ctx.send(error("No API key has been set."))
        except InvalidPlatform:
            return await ctx.send(
                error(
                    f"`{platform}` is not valid platform. Must be one of `pc`, `xbox` or `ps4`."
                )
            )
        except PlayerNotFound:
            return await ctx.send(error(f"`{username}` not found on `{platform}`."))

        await self.settings.set_username_platform(
            user=author, username=username, platform=platform
        )

        return await ctx.send(
            f"Set your username to `{username}` with the platform `{platform}` "
        )

    @is_owner()
    @_r6s.command()
    async def api(self, ctx, api_key):
        """
        Set the R6stats api key to be used.

        You can grab an api key from the r6stats.com Discord server.
        """
        conf_api_key = await self.config.apikey()

        if conf_api_key is not None:
            override = await self.yes_or_no(
                ctx, "You have already set your api key. Would you like to override?"
            )
            if not override:
                return await ctx.send("Api key has not been changed.")

        await self.config.apikey.set(api_key)

        return await ctx.send("Your api key has been set. ")

    @_r6s.command()
    async def ranked(self, ctx, username=None, platform=None):
        """
        Return your ranked stats for only regions played in Rainbow Six: Siege

        Examples:
            `[p]r6s ranked` - uses your profile username/platform
            `[p]r6s ranked bread pc` - uses specified username/platform
        """
        if username is None or platform is None:
            personal_stats = True
            username, platform = await self.settings.get_username_platform(ctx.author)
            if username is None or platform is None:
                return await ctx.send(
                    error(
                        f"You haven't setup your profile yet! Run: `{ctx.prefix}r6s profile <username> <platform>`"
                    )
                )

        api = GetApi(self.bot, self.config, username, platform)
        stats = await api.get_ranked_stats()
        max_rank, max_rank_image = await api.get_max_rank(stats["seasons"].items())
        played_region_stats = await api.get_valid_ranked(stats["seasons"].items())

        get_embed = StatsEmbed(username, platform, api)
        ranked_embed: discord.Embed = await get_embed.ranked_embed(
            stats, played_region_stats, max_rank_image
        )

        for region, stats in played_region_stats.items():
            if personal_stats:
                await self.settings.update_config_rank(
                    user=ctx.author, region=region, stats=stats
                )
                await self.settings.assign_rank_role(
                    user=ctx.author, guild=ctx.guild, rank=stats["rank"], region=region
                )

        await ctx.send(embed=ranked_embed)

    @_r6s.command()
    async def stats(self, ctx: commands.Context, username=None, platform=None):
        """
        Returns your Rainbow Six: Siege stats.

        By default the username / platform are retrieve from your profile, you can specify username and platform.

        Examples:
            `[p]r6s stats` - uses your profile username/platform
            `[p]r6s stats bread pc` - uses specified username/platform

        """
        if username is None or platform is None:
            username, platform = await self.settings.get_username_platform(ctx.author)
            personal_stats = True
            if username is None or platform is None:
                return await ctx.send(
                    error(
                        f"You haven't setup your profile yet! Run: `{ctx.prefix}r6s profile <username> <platform>`"
                    )
                )
        stats_embeds = []
        try:
            api: GetApi = GetApi(self.bot, self.config, username, platform)
            get_embed = StatsEmbed(username, platform, api)

            generic_stats = await api.get_generic_stats()
            all_ranked_stats = await api.get_ranked_stats()
            played_ranked_stats = await api.get_valid_ranked(
                all_ranked_stats["seasons"].items()
            )
            max_rank, max_rank_image = await api.get_max_rank(
                all_ranked_stats["seasons"].items()
            )

            if personal_stats:
                for region, stats in played_ranked_stats.items():
                    await self.settings.update_config_rank(
                        user=ctx.author, region=region, stats=stats
                    )
                    await self.settings.assign_rank_role(
                        user=ctx.author, guild=ctx.guild, rank=stats["rank"], region=region
                    )

            generic_embed: discord.Embed = await get_embed.generic_embed(generic_stats)
            ranked_embed: discord.Embed = await get_embed.ranked_embed(
                all_ranked_stats, played_ranked_stats, max_rank_image
            )
            aliases_embed: discord.Embed = await get_embed.alias_embed(generic_stats)

            stats_embeds.append(generic_embed)
            stats_embeds.append(ranked_embed)
            stats_embeds.append(aliases_embed)
        except PlayerNotFound:
            return await ctx.send(error(f"{username} not found on {platform}"))

        await menu(
            ctx,
            pages=stats_embeds,
            controls=DEFAULT_CONTROLS,
            message=None,
            page=0,
            timeout=30,
        )
