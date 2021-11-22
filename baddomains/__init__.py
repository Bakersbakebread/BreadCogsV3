from .baddomains import BadDomains


def setup(bot):
    cog = BadDomains(bot)
    bot.add_cog(cog)
