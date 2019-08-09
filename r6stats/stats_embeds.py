import discord
from datetime import datetime

from .assets.ranks import NAMES
from .api import GetApi


class StatsEmbed:
    def __init__(self, username, platform, api):
        self.username = username
        self.platform = platform
        self.api = api

    async def generic_embed(self, stats: dict) -> discord.Embed:
        progression = stats["progression"]
        general = stats["stats"]["general"]
        q = stats["stats"]["queue"]

        last_updated = datetime.fromisoformat(
            stats["last_updated"].replace("Z", "")
        ).strftime("%I%p %B %d %Y")

        description = (
            f"[Click here to view full stats](http://www.r6stats.com/stats/{stats['ubisoft_id']})\n\n"
            f"🏆 Level: `{progression['level']}`\n"
            f"🎲 Lootbox Probability: `{progression['lootbox_probability']}%`\n"
            f"⏲ Last updated: `{last_updated}`"
        )

        embed = discord.Embed(
            title=f"R6 Stats for {self.username} on {self.platform}",
            description=description,
        )
        embed.set_thumbnail(url=stats["avatar_url_146"])

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

        headshot_percent = (general["headshots"] / general["kills"]) * 100
        melee_percent = (general["melee_kills"] / general["kills"]) * 100
        suicide_percent = (general["suicides"] / general["deaths"]) * 100
        pen_percent = (general["penetration_kills"] / general["kills"]) * 100
        blind_percent = (general["blind_kills"] / general["kills"]) * 100

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

        embed.set_footer(text=f"⬅ Previous Page | ❌ Delete Embed | ➡ Next Page")

        return embed

    async def ranked_embed(
        self, all_stats: dict, played_region_stats: dict, max_rank_image: str
    ) -> discord.Embed:

        last_updated = datetime.fromisoformat(
            all_stats["last_updated"].replace("Z", "")
        ).strftime("%I%p %B %d %Y")
        description = (
            f"[Click here to view full stats](http://www.r6stats.com/stats/{all_stats['ubisoft_id']})\n"
            f"⏲ Last updated: `{last_updated}`"
        )
        ranked_embed = discord.Embed(
            title=f"Ranked stats for {self.username} on {self.platform}",
            description=description,
        )

        ranked_embed.set_thumbnail(url=max_rank_image)

        for region, stats in played_region_stats.items():
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
        ranked_embed.set_footer(text=f"⬅ Previous Page | ❌ Delete Embed | ➡ Next Page")
        return ranked_embed

    async def alias_embed(self, stats: dict):
        aliases_value = (
            f"**Found {len(stats['aliases'])} aliases for `{self.username}`**\n\n"
        )
        alias_embed = discord.Embed(title="📌 Aliases", description=aliases_value)

        for name in stats["aliases"]:
            seen_at = datetime.fromisoformat(
                name["last_seen_at"].replace("Z", "")
            ).strftime("%B %d %Y")
            alias_embed.add_field(
                name=name["username"], value=f"**Last seen: **`{seen_at}`"
            )
        alias_embed.set_footer(text=f"⬅ Previous Page | ❌ Delete Embed | ➡ Next Page")
        return alias_embed
