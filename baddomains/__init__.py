from .baddomains import BadDomains
from dislash import SlashClient

def setup(bot):
    cog = BadDomains(bot)
    bot.add_cog(cog)

    if not hasattr(bot, "slash"):
        bot.slash = SlashClient(bot)
