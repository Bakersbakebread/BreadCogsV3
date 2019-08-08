import discord
import aiohttp

from .exceptions import *
from .assets.ranks import ICONS

class GetApi:
    def __init__(self, bot, config, username, platform):
        self.bot = bot
        self.config = config
        self.username = username
        self.platform = platform
        self.platforms = ['pc', 'xbox', 'ps4']
        self.api_url = "https://api2.r6stats.com/public-api/stats/{username}/{platform}/{type}"

    async def get_generic_stats(self) -> dict:
        api_key = await self.config.apikey()
        if api_key is None:
            raise NoApiKey
        api_url = self.api_url.format(
                username = self.username,
                platform = self.platform,
                type = 'generic')

        headers = {'Authorization': f'Bearer {api_key}'}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(api_url) as resp:
                if resp.status == 200:
                    stats = await resp.json()
                    return stats
                if resp.status == 404:
                    raise PlayerNotFound

    async def get_ranked_stats(self) -> dict:
        api_key = await self.config.apikey()
        if api_key is None:
            raise NoApiKey
        api_url = self.api_url.format(
                username = self.username,
                platform = self.platform,
                type = 'seasonal')
        headers = {'Authorization': f'Bearer {api_key}'}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(api_url) as resp:
                if resp.status == 200:
                    stats = await resp.json()
                    return stats
                if resp.status == 404:
                    raise PlayerNotFound

    async def get_current_season(self, seasons: dict)-> dict:
        latest_entry = {}
        for season, value in seasons:
            latest_entry = {
                "ncsa" : value['regions']['ncsa'][0],
                "emea" : value['regions']['emea'][0],
                "apac" : value['regions']['apac'][0],
            }
            # stop after first iteration (latest season)
            break
        return latest_entry

    async def get_max_rank(self, seasons: dict) -> tuple:
        latest_entry = await self.get_current_season(seasons)
        ranks = []
        for k, v in latest_entry.items():
            ranks.append(v['rank'])
        return max(ranks), ICONS[max(ranks)]

    async def get_valid_ranked(self, seasons: dict) -> dict:
        played_regions = {}
        latest_entry = await self.get_current_season(seasons)
        for k, v in latest_entry.items():
            if v['wins'] > 0 and v['losses'] > 0:
                played_regions[k] = v
        return played_regions

    async def is_player(self, user):
        """Check to see if username/platform provided is found"""

        if self.platform.lower() not in [plat.lower() for plat in self.platforms]:
            raise InvalidPlatform

        generic_stats = await self.get_generic_stats()

        try:
            ubisoft_id = generic_stats['ubisoft_id']
            await self.config.user(user).ubisoft_id.set(ubisoft_id)
            return True
        except PlayerNotFound:
            return False
        except KeyError:
            return False






