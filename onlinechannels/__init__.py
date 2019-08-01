from .onlinechannels import OnlineChannels


def setup(bot):
    bot.add_cog(OnlineChannels(bot))
