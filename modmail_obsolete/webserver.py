from aiohttp import web
import aiohttp_jinja2
import jinja2
import aiohttp
import discord
import json
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

class WebServer:
    def __init__(self, bot, cog, config):
      self.app = web.Application()
      self.bot = bot
      self.port = 42356
      self.config = config
      self.handler = None
      self.runner = None
      self.site = None
      self.path = None
      self.cog = cog
      self.session = aiohttp.ClientSession()
    
    def unload(self):
      self.bot.loop.create_task(self.runner.cleanup())
      self.session.detach()
  
    async def home(self, request):
      response = aiohttp_jinja2.render_template("index.html", request, {})
      user = await self.config.user(await self.bot.get_user_info(280730525960896513)).info()
      print(user)
      return response
    
    async def make_webserver(self, path):

      self.path = path
      self.app.router.add_get("/", self.home)
      aiohttp_jinja2.setup(self.app,
          loader=jinja2.FileSystemLoader(str(self.path / "templates")))
      self.runner = web.AppRunner(self.app)
      await self.runner.setup()
      self.handler = self.app.make_handler()
      self.site = web.TCPSite(self.runner, "0.0.0.0", self.port)
      await self.site.start()
      print(f"Site running on: {self.site.name}")