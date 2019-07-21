from .channelcontent import ChannelContent


def setup(bot):
    bot.add_cog(ChannelContent(bot))
