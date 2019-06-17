from .modmail import Modmail


def setup(bot):
    c = Modmail(bot)
    bot.add_cog(c)
