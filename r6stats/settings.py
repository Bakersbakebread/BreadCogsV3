import discord

from .assets.ranks import NAMES

class R6StatsSettings:
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

    # player profile stuff
    async def get_username_platform(self, user: discord.Member) -> tuple:
        username = await self.config.user(user).username()
        platform = await self.config.user(user).platform()

        return username, platform

    async def set_username_platform(self, user: discord.Member, username: str, platform: str) -> None:
        await self.config.user(user).username.set(username)
        await self.config.user(user).platform.set(platform)

    async def update_config_rank(self, user: discord.Member, region: str, stats: dict) -> None:
        if region == 'ncsa' and stats['rank'] is not 0:
            await self.config.user(user).ncsa_rank.set(NAMES[stats['rank']])
        if region == 'emea' and stats['rank'] is not 0:
            await self.config.user(user).emea_rank.set(NAMES[stats['rank']])
        if region == 'apac' and stats['rank'] is not 0:
            await self.config.user(user).apac_rank.set(NAMES[stats['rank']])
