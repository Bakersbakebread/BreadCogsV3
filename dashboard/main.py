import discord

from redbot.core.commands import commands


class Dashboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self