from dislash import SlashClient

from .btnroles import BtnRoles


def setup(bot):
    cog = BtnRoles(bot)

    bot.add_cog(cog)

    # thanks Yami
    if not hasattr(bot, "slash"):
        bot.slash = SlashClient(bot)
