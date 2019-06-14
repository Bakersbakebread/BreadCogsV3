import discord
import json


class ModMailRpc:
  def __init__(self, bot, config):
    self.bot = bot
    self.config = config

  async def poing(self):
      response = {'test': 'success'}
      return json.dumps(response)

  async def get_all_messages(self):
    response = await self.config.all_guilds()
    return json.dumps(response)

  async def get_guilds_settings(self):
    response = []
    all_guilds = await self.config.all_guilds()

    for key, value in all_guilds.items():
        channel: discord.TextChannel = self.bot.get_channel(value['modmail_alerts_channel'])
        guild: discord.Guild = self.bot.get_guild(key)
        response.append({
                "guild": {
                    'name': guild.name,
                    'id': guild.id,
                    'icon': guild.icon_url._url,
                    'member_count': guild.member_count
                },
                "alerts_channel": {
                    'id': channel.id if channel is not None else None,
                    'name': channel.name if channel is not None else None
                },
                "alerts_active": value['modmail_alerts'],
                "thread_count": len(value['threads'])
        }
        )
    return json.dumps(response)
