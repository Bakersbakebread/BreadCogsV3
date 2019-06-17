import discord
import json
import redbot.core
from datetime import datetime
from redbot.core.utils.chat_formatting import humanize_timedelta
import psutil


class ModMailRpc:
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

    def get_uptime(self):
        time_delta = datetime.utcnow() - self.bot.uptime
        bot_uptime = humanize_timedelta(timedelta=time_delta)
        return bot_uptime

    async def poing(self):
        response = {"test": "success"}
        return json.dumps(response)

    async def get_bot_sys_stats(self):
        response = {
            "cpu": str(psutil.cpu_percent()),
            "ram": str(psutil.virtual_memory().percent),
            "guilds": len(self.bot.guilds),
            "shards": self.bot.shard_count,
            "cog_count": len(self.bot.commands),
            "uptime": self.get_uptime(),
            "red_version": redbot.core.__version__,
            "dpy_version": discord.__version__,
        }
        return json.dumps(response)

    async def get_all_messages(self):
        response = await self.config.all_guilds()
        return json.dumps(response)

    async def get_all_members(self):
        all_members = self.bot.get_all_members()
        response = []

        for x in all_members:
            roles = []
            if x.bot:
                continue
            for role in x.roles:
                y = {
                    "name": role.name,
                    "id": role.id,
                    "color": f"rgb({role.color.r}, {role.color.g}, {role.color.b})",
                }
                roles.append(y)
            created_at = x.created_at.strftime("%m/%d/%Y, %H:%M")
            joined_at = x.joined_at.strftime("%m/%d/%Y, %H:%M")
            # created_at_human = humanize_timedelta(timedelta = datetime.utcnow() - x.created_at)
            # joined_at_human = humanize_timedelta(timedelta = datetime.utcnow() - x.joined_at)
            y = {
                "member": {
                    "id": x.id,
                    "color": f"rgb({x.color.r}, {x.color.g}, {x.color.b})",
                    "name": x.name,
                    "discriminator": x.discriminator,
                    "avatar": str(x.avatar_url),
                    "created_at": created_at,
                    "joined_at": joined_at,
                    "guild": {"name": x.guild.name, "id": x.guild.id},
                    "roles": roles,
                }
            }
            response.append(y)
        return json.dumps(response)

    async def get_guilds_settings(self):
        response = []
        all_guilds = await self.config.all_guilds()
        for key, value in all_guilds.items():
            channel: discord.TextChannel = self.bot.get_channel(
                value["modmail_alerts_channel"]
            )
            guild: discord.Guild = self.bot.get_guild(key)
            print(guild.id)
            response.append(
                {
                    "guild": {
                        "name": guild.name,
                        "id": str(guild.id),
                        "icon": guild.icon_url._url,
                        "member_count": str(guild.member_count),
                    },
                    "alerts_channel": {
                        "id": str(channel.id) if channel is not None else None,
                        "name": channel.name if channel is not None else None,
                    },
                    "alerts_active": value["modmail_alerts"],
                    "thread_count": len(value["threads"]),
                }
            )
        return json.dumps(response)
