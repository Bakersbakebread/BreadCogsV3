from .modmail import Modmail

def setup(bot):
    bot.add_cog(Modmail(bot))