from .randomword import RandomWord

def setup(bot):
    cog = RandomWord(bot)
    bot.add_cog(cog)
