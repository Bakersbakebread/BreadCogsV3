from .r6stats import R6Stats


def setup(bot):
    bot.add_cog(R6Stats(bot))
