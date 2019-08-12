import discord
import asyncio

from .assets.ranks import NAMES
from .assets.roles import ROLES


class R6StatsSettings:
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.regions = {"emea": "EU", "apaca": "ASIA", "ncsa": "NA"}

    # player profile stuff
    async def get_username_platform(self, user: discord.Member) -> tuple:
        username = await self.config.user(user).username()
        platform = await self.config.user(user).platform()

        return username, platform

    async def set_username_platform(
        self, user: discord.Member, username: str, platform: str
    ) -> None:
        await self.config.user(user).username.set(username)
        await self.config.user(user).platform.set(platform)

    async def update_config_rank(
        self, user: discord.Member, region: str, stats: dict
    ) -> None:
        if region == "ncsa" and stats["rank"] is not 0:
            await self.config.user(user).ncsa_rank.set(NAMES[stats["rank"]])
        if region == "emea" and stats["rank"] is not 0:
            await self.config.user(user).emea_rank.set(NAMES[stats["rank"]])
        if region == "apac" and stats["rank"] is not 0:
            await self.config.user(user).apac_rank.set(NAMES[stats["rank"]])

    async def get_or_create_role(
        self, guild: discord.Guild, rank: int, role_name: str
    ) -> discord.Role:
        for role in guild.roles:
            if role_name in role.name:
                return role
        return await guild.create_role(
            reason="Creating rank role for R6Stats cog",
            color=discord.Color(ROLES[rank]["color"]),
            name=role_name,
        )

    async def purge_roles(
        self, region: str, guild: discord.guild, user: discord.Member
    ) -> None:
        all_role_names = [
            (r["name"].format(self.regions[region])) for k, r in ROLES.items()
        ]

        for role in guild.roles:
            try:
                if role.name in all_role_names:
                    await user.remove_roles(role, reason="R6Stats removing rank role")
            except IndexError:
                # role is not a r6stats rank role
                pass

    async def assign_rank_role(
        self, user: discord.Member, guild: discord.Guild, rank: int, region: str
    ):

        role_name = ROLES[rank]["name"].format(self.regions[region])
        role = await self.get_or_create_role(guild, rank, role_name)

        await user.add_roles(role, reason="R6Stats Rank Role")
