import discord

class ModMailSetup:
  def __init__(self, bot, context, config):
    self.bot = bot
    self.ctx = context
    self.config = config 
    self.category_name = "📬 ModMail"
    self.overwrites = {
            self.ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }

    self.green = discord.Color.green()
    self.orange = discord.Color.orange()
    self.red = discord.Color.red()
    
  def get_allowed_roles(self):
      roles = []
      for r in self.ctx.guild.roles:
          if r.permissions.manage_messages:
              roles.append(r)
      return roles
    
  async def setup(self):
    category = await self.create_category()
    await self.create_channels(category)
  
  async def create_channels(self, category):
    await self.ctx.guild.create_text_channel(
                name="Help", category=category
            )

    log_channel = await self.ctx.guild.create_text_channel(
                name="ModMail Log", category=category
            )
    await self.config.guild(self.ctx.guild).modmail_alerts_channel.set(log_channel.id)

  async def create_category(self):
    for role in self.get_allowed_roles():
        self.overwrites[role] = discord.PermissionOverwrite(read_messages=True)
    # create the category
    return await self.ctx.guild.create_category(
        name=self.category_name, overwrites=self.overwrites
    )