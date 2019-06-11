from aiohttp import web
import aiohttp_jinja2
import json
from redbot.core import Config
from aiohttp_json_rpc import JsonRpcClient
import json


config = Config.get_conf(None, identifier=13289648, cog_name="Test")

routes = web.RouteTableDef()


@routes.post('/')
async def home(request):
    # response = {"status":await config.threads()}
    # return web.Response(text=json.dumps(response), status=200)
    print(request.items)
    print(request.message)
    print(request.content)

    rpc_client = JsonRpcClient()
    try:
        await rpc_client.connect('127.0.0.1', 6133)
        call_result = await rpc_client.call("TEST__POING", ['test'])
        # prints 'pong' (if that's return val of ping)
    finally:
        await rpc_client.disconnect()
        return call_result


@routes.get('/test')
async def test(request):
    response = aiohttp_jinja2.render_template("index.html", request, {})
    return response
