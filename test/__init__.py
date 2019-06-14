from .test import Test

def setup(bot):
  c = Test(bot)
  bot.add_cog(c)
