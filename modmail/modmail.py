import discord
from datetime import datetime
from redbot.core import Config, commands
from redbot.core.data_manager import bundled_data_path

from aiohttp_json_rpc import JsonRpcClient
import json
import logging

import functools

from .utils import modmail_message_to_json, multi_guild_finder
from .webserver import WebServer
from .exceptions import *
from .setup import ModMailSetup
from .settings import ModMailSettings
from .rpc import ModMailRpc

from tabulate import tabulate
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.predicates import ReactionPredicate

log = logging.getLogger("red.breadcogs.modmail")


class Modmail(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.port = 42356
        self.config = Config.get_conf(
            self, identifier=13289648, force_registration=True
        )
        self.register_handlers()

        self.config.register_global(enforced_guild=None)

        self.config.register_guild(
            threads=[], modmail_alerts=True, modmail_alerts_channel=None
        )
        default_user = {
            "last_messaged": None,
            "guild_id": 0,
            "thread_is_open": False,
            "multi_guild_hold": False,
            "current_thread": 0,
            "blocked": False,
        }

        self.config.register_user(**default_user)

        #
        # SETUP WEB-SERVER
        #
        self.web = WebServer(self.bot, self, self.config)
        self.web_task = self.bot.loop.create_task(self.web.make_webserver(self.port))

    def register_handlers(self):
        # TODO: Refactor to list
        x = ModMailRpc(self.bot, self.config)
        self.bot.register_rpc_handler(x.poing)
        self.bot.register_rpc_handler(x.get_all_messages)
        self.bot.register_rpc_handler(x.get_guilds_settings)
        self.bot.register_rpc_handler(x.get_all_members)
        self.bot.register_rpc_handler(x.get_bot_sys_stats)

    async def is_user_valid(self, user: discord.User):
        blocked = await self.config.user(user).get_raw("blocked")
        if blocked:
            raise UserIsBlocked
        thread_open = await self.config.user(user).get_raw("thread_is_open")
        if thread_open:
            raise UserIsWaitingForReply
        multi_guild_hold = await self.config.user(user).get_raw("multi_guild_hold")
        if multi_guild_hold:
            raise UserNotChosenGuild
        return True

    async def shared_guilds_check(self, author: discord.User) -> discord.Guild:
        """
        Sends Embed Reaction table to determine where to send modmail message
        """
        await self.config.user(author).set_raw("multi_guild_hold", value=True)
        shared_guilds = await multi_guild_finder(self.bot.get_all_members(), author)

        # only one guild, so let's stop here
        if len(shared_guilds) == 1:
            return shared_guilds[0]

        table = [[index, guild] for index, guild in enumerate(shared_guilds)]
        await author.send(
            "We have more than one server in common, please choose from list below where you would like to send the message."
        )
        msg = await author.send(f"```{tabulate(table, tablefmt='presto')}```")

        emojis = ReactionPredicate.NUMBER_EMOJIS[: len(shared_guilds)]
        start_adding_reactions(msg, emojis)
        pred = ReactionPredicate.with_emojis(emojis, msg)
        await self.bot.wait_for("reaction_add", check=pred)

        guild = shared_guilds[pred.result]
        await msg.delete()
        await self.config.user(author).set_raw("multi_guild_hold", value=False)
        return guild

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if not isinstance(message.channel, discord.abc.PrivateChannel):
            return
        try:
            await self.is_user_valid(message.author)
        except UserIsBlocked:
            log.info(
                f"Blocked user attempted to send modmail ({message.author.name}-{message.author.id})"
            )
            return await message.author.send(
                "⛔️ You have been blocked from sending mail."
            )
        except UserIsWaitingForReply:
            return await message.author.send(
                "💬 Please wait for a reply before sending another mail."
            )
        except UserNotChosenGuild:
            return await message.author.send(
                "📣 Please choose a guild you wish to send your mail too."
            )

        if await self.config.enforced_guild() is not None:
            guild = self.bot.get_guild(await self.config.enforced_guild())
        else:
            guild = await self.shared_guilds_check(message.author)

        channel_from_config = await self.config.guild(guild).modmail_alerts_channel()
        channel = self.bot.get_channel(channel_from_config)
        if channel is None:
            log.error(
                f"ModMail not setup: {message.author.name} attempted modmail to {guild}"
            )
            return await message.author.send(
                f"⛔️ `{guild.name}` has not been setup to recieve modmail."
            )

        alert_message = await self.send_alert(channel, message)
        json_message = await modmail_message_to_json(message, alert_message)
        await self.add_thread(guild, json_message)
        await message.author.send(f"✅ Your message has been sent to `{guild.name}`.")
        log.info(
            f"New modmail message from {message.author.name} ({message.author.id}) to {guild.name}"
        )

    async def send_alert(self, channel: discord.TextChannel, message: discord.Message):
        author = message.author

        if message.attachments:
            attachments_string = f"**Attachments**\n {message.attachments.url}"
        else:
            attachments_string = f" "

        description = (
            f"**Author** \n"
            f" `{author.name}#{author.discriminator}` \n"
            f" `{author.id}` "
            f"```{message.content}```\n"
            f"{attachments_string}"
        )
        embed = discord.Embed(
            title="📬 New ModMail recieved",
            description=description,
            color=discord.Color.green(),
        )
        msg = await channel.send(embed=embed)
        return msg

    async def add_thread(self, guild: discord.Guild, modmail_message: dict):
        guild_group = self.config.guild(guild)
        async with guild_group.threads() as threads:
            threads.append(modmail_message)

    @commands.command()
    async def rpc(self, ctx, message):
        await ctx.send("Creating RPC Client")
        rpc_client = JsonRpcClient()
        await ctx.send("Created success, trying to connect")
        try:
            await rpc_client.connect("127.0.0.1", 6133)
            await ctx.send("Connected")
            call_result = await rpc_client.call("GET_METHODS")
            # prints 'pong' (if that's return val of ping)
            await ctx.send("Response:")
            await ctx.send(call_result)
        finally:
            await ctx.send("Closing RPC Client")
            await rpc_client.disconnect()

    @commands.group()
    async def t(self, ctx):
        response = []
        all_guilds = await self.config.all_guilds()

        for key, value in all_guilds.items():
            channel: discord.TextChannel = self.bot.get_channel(
                value["modmail_alerts_channel"]
            )
            guild: discord.Guild = self.bot.get_guild(key)
            response.append(
                {
                    key: {
                        "guild": {
                            "name": guild.name,
                            "icon": guild.icon_url._url,
                            "member_count": guild.member_count,
                        },
                        "alerts_channel": {
                            "id": channel.id if channel is not None else None,
                            "name": channel.name if channel is not None else None,
                        },
                        "alerts_active": value["modmail_alerts"],
                        "thread_count": len(value["threads"]),
                    }
                }
            )
        for x in response:
            await ctx.send(x)

    @commands.group()
    async def modmail(self, ctx):
        pass

    #
    # SETUP
    #
    @modmail.group()
    async def create(self, ctx):
        try:
            await ModMailSetup(self.bot, ctx, self.config).setup()
            log.info(f"Modmail created in {ctx.guild.name}-{ctx.guild.id}")
        except discord.errors.Forbidden:
            log.exception(
                "Modmail could not be created as missing manage channels permission."
            )
            return await ctx.send("⛔ Missing `Manage Channels` permission.")

    #
    # SETTINGS
    #
    @modmail.group(name="set")
    async def _set(self, ctx):
        pass

    @_set.group(name="channel")
    async def _set_channel(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        try:
            channels = await ModMailSettings(self.bot, ctx, self.config).set_channel(
                channel
            )
        except AlertsChannelExists:
            return await ctx.send(
                f":mailbox_with_mail: Already sending ModMail alerts to `{channel.name}` "
            )

        await ctx.send(
            f":mailbox_with_mail: ModMail alerts channel changed from ` {channels[0]} ` to ` {channels[1]} `"
        )

    @_set.group(name="guild", autohelp=False)
    async def _set_enforced_guild(self, ctx, guild=None):
        if guild is None:
            guild = ctx.guild.id

        try:
            get_guild = self.bot.get_guild(int(guild))
        except ValueError:
            return await ctx.send(f'⛔ `{guild}` is not a valid guild ID.')

        if get_guild is None:
            return await ctx.send(f'⛔ `{guild}` is not a valid guild ID. ')

        else:
            enforced_guild = await ModMailSettings(
                self.bot, ctx, self.config).set_enforced_guild(int(guild))

        await ctx.send(f":mailbox_with_mail: Enforced guild set to `{enforced_guild[1]}`")

    @_set.group(name="enforce", autohelp=False)
    async def _toggle_enforced_guild(self, ctx):
        if await self.config.enforced_guild() is None:
            return await ctx.send('Not enforcing one guild.')

        unforce_guild = await ModMailSettings(self.bot, ctx, self.config).set_enforced_guild(None)
        await ctx.send(f':mailbox_with_mail: Disabled single guild enforcement.')

    @_set.group(name="alerts")
    async def _set_alerts_toggle(self, ctx):
        alerts = await ModMailSettings(self.bot, ctx, self.config).set_alerts()
        if alerts:
            await ctx.send(f":mailbox_with_mail::bell: ModMail alerts `enabled` ")
        else:
            await ctx.send(f":mailbox_with_mail::no_bell: ModMail alerts `disabled`")

    #
    # BLOCKING
    #
    @modmail.group(name="block")
    async def _block_user(self, ctx, user: discord.User):
        if user == ctx.me:
            return await ctx.send(":no_entry: It wouldn't be a good idea to block me.")
        if await self.config.user(user).blocked():
            return await ctx.send(f":mute: `{user.name}` is already blocked.")
        await self.config.user(user).blocked.set(True)
        await ctx.send(f":mute: `{user.name}` has been blocked.")

    @modmail.group(name="unblock")
    async def _unblock_user(self, ctx, user: discord.User):
        if not await self.config.user(user).blocked():
            return await ctx.send(f":loud_sound: `{user.name}` is not blocked.")
        await self.config.user(user).blocked.set(False)
        await ctx.send(f":loud_sound: `{user.name}` has been unblocked.")
