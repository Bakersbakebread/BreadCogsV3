from .main import ChannelArchive


def setup(bot):
    cog = ChannelArchive(bot)
    bot.add_cog(cog)
