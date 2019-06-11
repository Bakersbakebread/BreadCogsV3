from aiohttp import web
import aiohttp_jinja2
import json
from redbot.core import Config

config = Config.get_conf(None, identifier=13289648, cog_name="Test")

routes = web.RouteTableDef()
    
@routes.get('/')
async def home(request):
    response = {"status":await config.threads()}
    return web.Response(text=json.dumps(response), status=200)

@routes.get('/test')
async def test(request):
    response = aiohttp_jinja2.render_template("index.html", request, {})
    return response