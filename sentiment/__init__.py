from .sentiment import Sentiment

def setup(bot):
    bot.add_cog(Sentiment(bot))
