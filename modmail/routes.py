from aiohttp import web
from aiohttp_session import get_session
import aiohttp
import aiohttp_jinja2
import json
from redbot.core import Config
from aiohttp_json_rpc import JsonRpcClient
import logging

log = logging.getLogger("red.breadcogs.modmail.rpc")

config = Config.get_conf(None, identifier=13289648, cog_name="Test")

routes = web.RouteTableDef()

CLIENT_ID = 492019114924048394
CLIENT_SECRET = "rQNWzDLRUcpsdhI4glYRkY3JBwO6WBl-"
REDIRECT_URI = "http://localhost:42356/api/discord/callback"


async def rpc_call(method, params):
    rpc_client = JsonRpcClient()
    try:
        await rpc_client.connect("127.0.0.1", 6133)
        call_result = await rpc_client.call(method, params)
        return call_result
    except Exception as e:
        print(e)
    finally:
        await rpc_client.disconnect()


async def exchange_code(code):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "scope": "identify email connections",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    session = aiohttp.ClientSession()
    async with session.post(
        url="https://discordapp.com/api/oauth2/token", data=data, headers=headers
    ) as r:
        r = await r.json()
        await session.close()
        return r


async def get_discord_user(token):
    session = aiohttp.ClientSession()
    user = await session.get(
        "https://discordapp.com/api/v6/users/@me",
        headers={"Authorization": f"Bearer {token}"},
    )
    user_data = await user.json()
    await session.close()
    return user_data


@routes.get("/api/discord/login")
async def _discord_login(request):
    return web.HTTPFound(
        "https://discordapp.com/api/oauth2/authorize?client_id=492019114924048394&redirect_uri=http%3A%2F%2Flocalhost%3A42356%2Fapi%2Fdiscord%2Fcallback&response_type=code&scope=identify%20email%20connections%20guilds"
    )


@routes.get("/api/discord/callback")
async def _discord_callback(request):
    session = await get_session(request)
    code = request.rel_url.query["code"]
    token = await exchange_code(code)
    user = await get_discord_user(token["access_token"])
    session["token"] = token["access_token"]
    session["user"] = user

    return web.HTTPFound(location=request.app.router["root"].url_for())


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


@routes.get("/api/login-status")
async def _login_status(request):
    """
    Returns session details to front-end
    """
    session = await get_session(request)
    try:
        user = {"token": session["token"]}
    except KeyError:
        return web.Response(text="Not logged in", status=403)
    return web.Response(text=json.dumps(user), status=200)


@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        if response.status != 404:
            return response
        message = response.message
    except web.HTTPException as ex:
        if ex.status != 404:
            raise
        else:
            return web.HTTPFound(location=request.app.router["root"].url_for())
        message = ex.reason
    return web.json_response({"error": message})


@routes.get("/", name="root")
async def _test(request):
    # session = await get_session(request)
    # if 'user' not in session:
    #     # add check_guilds here, if ID in role_list, continue
    #     response = web.Response(text="NO")
    #     return response
    response = aiohttp_jinja2.render_template("index.html", request, {})
    return response
