import discord

import logging
from datetime import datetime

from .exceptions import *
from .settings import R6StatsSettings
from .api import GetApi
from .assets.ranks import NAMES

from redbot.core import Config, commands
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.chat_formatting import error


class R6Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=41398865, force_registration=True)
        self.config.register_user(
            username=None,
            platform=None,
            ubisoft_id=None,
            emea_rank=None,
            ncsa_rank=None,
            apac_rank=None
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

    @commands.command()
    async def profile(self, ctx, username, platform):
        author = ctx.author
        conf_username, conf_platform = await self.settings.get_username_platform(author)

        if conf_username or conf_platform is not None:
            override = await self.yes_or_no(
                ctx, "You have already set your username and platform. Would you like to override?"
            )
            if not override:
                return await ctx.send(
                    f"Okay. Keeping the following details:"
                    f"\nUsername: `{conf_username}`"
                    f"\nPlatform: `{conf_platform}`")

        try:
            is_player = await GetApi(self.bot, self.config, username, platform).is_player(author)
        except NoApiKey:
            return await ctx.send(error("No API key has been set."))
        except InvalidPlatform:
            return await ctx.send(error(f"`{platform}` is not valid platform. Must be one of `pc`, `xbox` or `ps4`."))
        except PlayerNotFound:
            return await ctx.send(error(f"`{username}` not found on `{platform}`."))

        await self.settings.set_username_platform(user=author, username=username, platform=platform)

        return await ctx.send(f'Set your username to `{username}` with the platform `{platform}` ')

    @commands.command()
    async def api(self, ctx, api_key):
        conf_api_key = await self.config.apikey()

        if conf_api_key is not None:
            override = await self.yes_or_no(
                ctx, "You have already set your api key. Would you like to override?"
            )
            if not override:
                return await ctx.send("Api key has not been changed.")

        await self.config.apikey.set(api_key)

        return await ctx.send("Your api key has been set. ")

    @commands.command()
    async def ranked(self, ctx, username=None, platform=None):
        if username is None or platform is None:
            personal_stats = True
            username, platform = await self.settings.get_username_platform(ctx.author)
            if username is None or platform is None:
                return await ctx.send(
                    error(f"You haven't setup your profile yet! Run: `{ctx.prefix}r6s profile <username> <platform>`"))

        api = GetApi(self.bot, self.config, username, platform)
        stats = await api.get_ranked_stats()
        max_rank, max_rank_image = await api.get_max_rank(stats['seasons'].items())

        played_region_stats = await api.get_valid_ranked(stats['seasons'].items())

        last_updated = datetime.fromisoformat(stats['last_updated'].replace("Z", "")).strftime("%I%p %B %d %Y")
        description = (
            f"[Click here to view full stats](http://www.r6stats.com/stats/{stats['ubisoft_id']})\n"
            f"⏲ Last updated: `{last_updated}`"
        )
        ranked_embed = discord.Embed(
            title=f"Ranked stats for {username} on {platform}",
            description=description)

        ranked_embed.set_thumbnail(url=max_rank_image)

        for region, stats in played_region_stats.items():
            if personal_stats:
                await self.settings.update_config_rank(
                    user=ctx.author,
                    region=region,
                    stats=stats
                )


            kd_value = (
                f"**Wins:** ⠀`{stats['wins']}`\n"
                f"**Losses:**⠀`{stats['losses']}`\n"
                f"⇒ Abandons:⠀`{stats['abandons']}`\n"
                f"**W/L:**   ⠀`{(stats['wins'] / stats['losses']):.2f}`\n\n"
                f"**Rank:** `{stats['rank_text']}`\n"
                f"**MMR:**  `{stats['mmr']}`\n"
                f"⇒ Max rank: `{NAMES[stats['max_rank']]}`\n"
                f"⇒ Max MMR: `{stats['max_mmr']}`\n"
            )
            ranked_embed.add_field(name=region, value=kd_value)

        await ctx.send(embed=ranked_embed)

    @commands.command()
    async def stats(self, ctx: commands.Context, username=None, platform=None):
        if username is None or platform is None:
            username, platform = await self.settings.get_username_platform(ctx.author)
            if username is None or platform is None:
                return await ctx.send(
                    error(f"You haven't setup your profile yet! Run: `{ctx.prefix}r6s profile <username> <platform>`")
                )

        try:
            stats = await GetApi(self.bot, self.config, username, platform).get_generic_stats()
        except PlayerNotFound:
            return await ctx.send(error(f"{username} not found on {platform}"))

        progression = stats['progression']
        general = stats['stats']['general']
        q = stats['stats']['queue']

        last_updated = datetime.fromisoformat(stats['last_updated'].replace("Z", "")).strftime("%I%p %B %d %Y")

        description = (
            f"[Click here to view full stats](http://www.r6stats.com/stats/{stats['ubisoft_id']})\n\n"
            f"🏆 Level: `{progression['level']}`\n"
            f"🎲 Lootbox Probability: `{progression['lootbox_probability']}%`\n"
            f"⏲ Last updated: `{last_updated}`"
        )

        embed = discord.Embed(title=f"R6 Stats for {username} on {platform}", description=description)
        embed.set_thumbnail(url=stats['avatar_url_146'])

        kd_value = (
            f"**Kills:** ⠀`{general['kills']}`\n"
            f"⇒ Casual: `{q['casual']['kills']}`\n⇒ Ranked: `{q['ranked']['kills']}`\n"
            f"**Deaths:**⠀`{general['deaths']}`\n"
            f"⇒ Casual: `{q['casual']['deaths']}`\n⇒ Ranked: `{q['ranked']['deaths']}`\n"
            f"**K/D:**   ⠀`{general['kd']:.2f}`\n"
            f"⇒ Casual: `{q['casual']['kd']}`\n⇒ Ranked: `{q['ranked']['kd']}`\n\n"
        )
        embed.add_field(name="🔫 K / D", value=kd_value)

        wl_value = (
            f"**Wins:**  ⠀`{general['wins']}` \n"
            f"⇒ Casual: `{q['casual']['wins']}`\n⇒ Ranked: `{q['ranked']['wins']}`\n"
            f"**Losses:**⠀`{general['losses']}`\n"
            f"⇒ Casual: `{q['casual']['losses']}`\n⇒ Ranked: `{q['ranked']['losses']}`\n"
            f"**W/L:**   ⠀`{general['wl']:.2f}`\n"
            f"⇒ Casual: `{q['casual']['wl']}`\n⇒ Ranked: `{q['ranked']['wl']}`\n"
        )
        embed.add_field(name="🏅 W / L", value=wl_value)

        headshot_percent = (general['headshots'] / general['kills']) * 100
        melee_percent = (general['melee_kills'] / general['kills']) * 100
        suicide_percent = (general['suicides'] / general['deaths']) * 100
        pen_percent = (general['penetration_kills'] / general['kills']) * 100
        blind_percent = (general['blind_kills'] / general['kills']) * 100

        general2_value = (
            f"_Percentage is stat/kills_\n"
            f"**Headshots:** ⠀`{general['headshots']} ({headshot_percent:.2f}%)`\n"
            f"**Melees:**   ⠀`{general['melee_kills']} ({melee_percent:.2f}%)`\n"
            f"**Wallbangs:**   ⠀`{general['penetration_kills']} ({pen_percent:.2f}%)`\n"
            f"**Blind kills:**   ⠀`{general['blind_kills']} ({blind_percent:.2f}%)`\n"
            f"**Suicides:**⠀`{general['suicides']} ({suicide_percent:.2f}% of deaths)`\n"
        )
        embed.add_field(name="⚰ Kill stats", value=general2_value)

        misc_value = (
            f"**Gadgets destroyed:** ⠀`{general['gadgets_destroyed']}`\n"
            f"**Games played:**   ⠀`{general['games_played']}`\n"
            f"**Rappel breaches:**   ⠀`{general['rappel_breaches']}`\n"
            f"**Reinforced walls:**   ⠀`{general['reinforcements_deployed']}`\n"
            f"**Revives:**⠀`{general['revives']}`\n"
        )

        embed.add_field(name="👉🏼 Misc. stats", value=misc_value)

        embed.add_field(name="React for more", value=f"📌 - Aliases | 🎖 - Ranked")

        aliases_value = (
            f"**Found {len(stats['aliases'])} aliases for `{username}`**\n\n"
        )
        alias_embed = discord.Embed(title="📌 Aliases", description=aliases_value)

        for name in stats['aliases']:
            seen_at = datetime.fromisoformat(name['last_seen_at'].replace("Z", "")).strftime("%B %d %Y")
            alias_embed.add_field(
                name=name['username'],
                value=f"**Last seen: **`{seen_at}`")

        msg = await ctx.send(embed=embed)
        start_adding_reactions(msg, ['📌', '🎖'])

        def check(reaction, user):
            return user == ctx.author

        reaction, user = await ctx.bot.wait_for("reaction_add", check=check)
        if str(reaction.emoji) == '📌':
            await ctx.send(embed=alias_embed)
        if str(reaction.emoji) == '🎖':
            await ctx.invoke(self.bot.get_cog('R6Stats').ranked)
        await msg.clear_reactions()
