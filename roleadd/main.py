import discord

from redbot.core.config import Config
from redbot.core.commands import commands


class RoleAdd:
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=12903810928309)

