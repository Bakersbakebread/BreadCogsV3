import discord
import asyncio

from redbot.core import Config, commands

ROLES = {
    "eu": 594337862040944670,
    "na": 594337979947024413,
    "east_coast": 606474338803122176,
    "west_coast": 606474468977803286,
    "canada": 606516770928459796,
    "central": 606516159742738461,
}

CHANNEL_NAMES = {
    "total": "total online - {}",
    "eu": "🌍 EU - {}",
    "na": "🌎 NA - {}",
    "canada": "🍁 CAN - {}",
    "west_coast": "👈 WEST - {}",
    "east_coast": "👉 EAST - {}",
    "central": "🖖 CENT - {}",
}


class OnlineChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.task_to_cancel = self.bot.loop.create_task(self.bg_task())
        self.total_online = []
        self.roles_online_default = {
            "eu": [],
            "na": [],
            "east_coast": [],
            "west_coast": [],
            "canada": [],
            "central": [],
        }
        self.roles_online = {
            "eu": [],
            "na": [],
            "east_coast": [],
            "west_coast": [],
            "canada": [],
            "central": [],
        }
        self.guild = self.bot.get_guild(561619840377552896)

    def cog_unload(self):
        self.task_to_cancel.cancel()

    async def bg_task(self):
        while True:
            n = 60
            await self.check_online_status(self.guild)
            await self.update_channels()
            await asyncio.sleep(n)

    async def update_channels(self):
        #edit category
        category = self.guild.get_channel(606534494698078220)
        await category.edit(name=CHANNEL_NAMES['total'].format(len(self.total_online)))

        #edit channels
        for key, member_list in self.roles_online.items():
            member_names = [m.name for m in member_list]
            for channel in self.guild.channels:
                if any(word in channel.name.lower() for word in key.lower().split("_")):
                    await channel.edit(
                        name=CHANNEL_NAMES[key].format(len(member_names))
                    )

    @commands.command()
    async def refresh(self, ctx):
        await self.check_online_status(ctx.guild)
        cat = ctx.guild.get_channel(606534494698078220)
        await cat.edit(name=CHANNEL_NAMES['total'].format(len(self.total_online)))
        for key, member_list in self.roles_online.items():
            member_names = [m.name for m in member_list]
            await ctx.send(f"{key}: {len(member_names)}")
            for channel in ctx.guild.channels:
                if any(word in channel.name.lower() for word in key.lower().split("_")):
                    await ctx.send(f"editing: {channel}")
                    await channel.edit(
                        name=CHANNEL_NAMES[key].format(len(member_names))
                    )

        await ctx.send(len(self.total_online))

    async def check_online_status(self, guild):
        # guild = self.bot.get_guild(561619840377552896)
        self.total_online = []
        self.roles_online = self.roles_online_default
        all_members = [m for m in guild.members]
        for member in all_members:
            member_roles = [role.id for role in member.roles]
            if member.status.value == "online":
                self.total_online.append(member)
                for role_name, role_id in ROLES.items():
                    if role_id in member_roles:
                        self.roles_online[role_name].append(member)
