from .textclass import TextClass


def setup(bot):
    bot.add_cog(TextClass(bot))
