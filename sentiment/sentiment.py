import discord
from redbot.core import commands
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# from chatterbot import ChatBot
# from chatterbot.trainers import ChatterBotCorpusTrainer
# import asyncio

# chatbot = ChatBot("AlfredTwo")
# trainer = ChatterBotCorpusTrainer(chatbot)

# trainer.train(
#     "chatterbot.corpus.english"
# )


class Sentiment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.analyser = SentimentIntensityAnalyzer()

    @commands.command()
    async def create(self, ctx):
        await ctx.send('Good job!')

    # def sentiment_analyzer_scores(self, text):
    #     score = self.analyser.polarity_scores(text)
    #     lb = score['compound']
    #     if lb >= 0.05:
    #         return 1
    #     elif (lb > -0.05) and (lb < 0.05):
    #         return 0
    #     else:
    #         return -1

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     if isinstance(message.channel, discord.abc.PrivateChannel):
    #         return
    #     if message.author.id == 352832284354674692:
    #         return
    #     await asyncio.sleep(5)
    #     sentiment = self.sentiment_analyzer_scores(message.content)
    #     # await message.channel.send(a)
    #     if message.author.id == 280730525960896513 or 432500921080217600:
    #         if message.channel.id == 582991817751134218:
    #             if sentiment == 1:
    #                 await message.add_reaction("\N{HEAVY PLUS SIGN}")
    #             if sentiment < 0:
    #                 await message.add_reaction("\N{HEAVY MINUS SIGN}")
    #             response = chatbot.get_response(message.content)

    #             await message.channel.send(response)
    #             print(f"MSG: [{message.content}] REPLY: [{response}]")
