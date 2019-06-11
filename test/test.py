import discord
from redbot.core import Config, commands
from redbot.core.data_manager import bundled_data_path
from .webserver import WebServer
from .models import ModmailThread

import json

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.port = 42356
        self.config = Config.get_conf(self, identifier=13289648)
        
        self.config.register_global(
            threads = []
        )
        self.web = WebServer(self.bot, self, self.config)
        self.web_task = self.bot.loop.create_task(
            self.web.make_webserver(self.port))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        x = {"author":message.author.name, "content":message.content}
        await self.add_thread(x)
        # await message.channel.send(x)

    async def add_thread(self, thread):
        async with self.config.threads() as threads:
            threads.append(thread)
