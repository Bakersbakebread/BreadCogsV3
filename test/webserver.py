from aiohttp import web
import aiohttp_jinja2
import jinja2
import aiohttp
import discord
import json
import os
from redbot.core.data_manager import bundled_data_path
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from .routes import routes


class WebServer:
    def __init__(self, bot, cog, config):
        self.app = web.Application()
        self.bot = bot
        self.port = 42356
        self.handler = None
        self.runner = None
        self.site = None
        self.path = None
        self.cog = cog
        self.config = config
        self.path = bundled_data_path(self)
        print(self.config)
        self.session = aiohttp.ClientSession()
    
    def unload(self):
        self.bot.loop.create_task(self.runner.cleanup())
        self.session.detach()
    
    @routes.get('/p')
    async def p(self, request):
        async with self.config.threads() as threads:
            print(threads)
            return web.Response(text=json.dumps(threads), status=200)
    

    async def make_webserver(self, port):
        self.app.add_routes(routes)
        self.app.router.add_static('/', str(self.path) + "/client/dist", name="static")
        aiohttp_jinja2.setup(self.app,
                             loader=jinja2.FileSystemLoader(str(self.path) + "/client/dist"),
                             default_helpers=True)

        self.runner = web.AppRunner(self.app)
        await self.runner.setup()

        self.handler = self.app.make_handler()
        self.site = web.TCPSite(self.runner, "0.0.0.0", port)
        await self.site.start()
        print(f"Site running on: {self.site.name}")
