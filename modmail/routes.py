from aiohttp import web

import aiohttp_jinja2
import json
from redbot.core import Config
from aiohttp_json_rpc import JsonRpcClient
import logging

log = logging.getLogger("red.breadcogs.modmail.rpc")

config = Config.get_conf(None, identifier=13289648, cog_name="Test")

routes = web.RouteTableDef()


async def rpc_call(method, params):
    rpc_client = JsonRpcClient()
    try:
        await rpc_client.connect("127.0.0.1", 6133)
        call_result = await rpc_client.call(method, params)
        # prints 'pong' (if that's return val of ping)
    except Exception as e:
        print(e)
    finally:
        await rpc_client.disconnect()
        return call_result


@routes.post("/bot/sys-settings")
async def _sys_settings(request):
    """
    Returns system settings of bot instance,
    including CPU & RAM usage
    """
    response = await rpc_call("MODMAILRPC__GET_BOT_SYS_STATS", [])
    return web.Response(text=json.dumps(response), status=200)


@routes.post("/guilds/settings")
async def _guild_settings(request):
    """
    Returns settings about guilds,
    such as alerts enabled and where to send
    """
    response = await rpc_call("MODMAILRPC__GET_GUILDS_SETTINGS", [])
    return web.Response(text=json.dumps(response), status=200)


@routes.post("/guilds/all-messages")
async def _get_all_messages(request):
    """
    Returns all modmail messages from config
    """
    response = await rpc_call("MODMAILRPC__GET_ALL_MESSAGES", [])
    return web.Response(text=json.dumps(response), status=200)


@routes.post("/members/get-all-short")
async def _all_members_short(request):
    """
    Returns dict of all members bot can see,
    this is a minified list of self.bot.get_all_members()
    """
    response = await rpc_call("MODMAILRPC__GET_ALL_MEMBERS", [])
    return web.Response(text=json.dumps(response), status=200)


@routes.get("/test")
async def _test(request):
    response = aiohttp_jinja2.render_template("index.html", request, {})
    return response
