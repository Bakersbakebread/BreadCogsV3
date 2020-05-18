from .main import TeamShuffle


def setup(bot):
    cog = TeamShuffle(bot)
    bot.add_cog(cog)

