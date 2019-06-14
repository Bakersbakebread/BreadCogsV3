from aiohttp import web
import aiohttp_jinja2
import jinja2
import aiohttp
import discord
import json
import os
import logging
from redbot.core.data_manager import bundled_data_path
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from .routes import routes
log = logging.getLogger('red.breadcogs.modmail.webserver')

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
        self.session = aiohttp.ClientSession()

    def unload(self):
        self.bot.loop.create_task(self.runner.cleanup())
        self.session.detach()

    async def make_webserver(self, port):
        log.info('Attempting to start server')
        self.app.add_routes(routes)
        log.info('add routes')
        self.app.router.add_static(
            "/", str(self.path) + "/client/dist", name="static")
        
        log.info('add static')
        aiohttp_jinja2.setup(
            self.app,
            loader=jinja2.FileSystemLoader(str(self.path) + "/client/dist"),
            default_helpers=True,
        )
        
        log.info('jinja2 setup')

        self.runner = web.AppRunner(self.app)
        log.info('self.runner')
        await self.runner.setup()
        log.info('await self.runner')

        self.handler = self.app.make_handler()
        log.info('self.handler')
        self.site = web.TCPSite(self.runner, "0.0.0.0", self.port)
        log.info('self.tcpsite - attempting to start')
        await self.site.start()
        log.info(f"Site running on: {self.site.name}")
