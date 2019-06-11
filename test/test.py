import discord
from redbot.core import Config, commands
from redbot.core.data_manager import bundled_data_path
from .webserver import WebServer
from .models import ModmailThread
from aiohttp_json_rpc import JsonRpcClient
import json


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.port = 42356
        self.config = Config.get_conf(self, identifier=13289648)

        self.config.register_global(
            threads=[]
        )
        self.web = WebServer(self.bot, self, self.config)
        self.web_task = self.bot.loop.create_task(
            self.web.make_webserver(self.port))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        x = {"author": message.author.name, "content": message.content}
        await self.add_thread(x)
        # await message.channel.send(x)

    async def poing(self, message):
        # response = [
        #     member.guild.name for member in self.bot.get_all_members() if member.id == 280730525960896513
        # ]
        test = discord.utils.get(self.bot.users, id=280730525960896513)
        await test.send(message)
        response = test.name
        return response

    @commands.command()
    async def rpc(self, ctx, message):
        await ctx.send('Creating RPC Client')
        rpc_client = JsonRpcClient()
        await ctx.send('Created success, trying to connect')
        try:
            await rpc_client.connect('127.0.0.1', 6133)
            await ctx.send('Connected')
            call_result = await rpc_client.call("TEST__POING", [message])
            # prints 'pong' (if that's return val of ping)
            await ctx.send('Response:')
            await ctx.send(call_result)
        finally:
            await ctx.send('Closing RPC Client')
            await rpc_client.disconnect()

    async def add_thread(self, thread):
        async with self.config.threads() as threads:
            threads.append(thread)
