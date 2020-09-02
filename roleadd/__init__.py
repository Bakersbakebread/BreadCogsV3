from .main import RoleAdd


def setup(bot):
    cog = RoleAdd(bot)
    bot.add_cog(cog)
