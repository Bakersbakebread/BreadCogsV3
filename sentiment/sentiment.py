import discord
from redbot.core import commands
from random import shuffle
import sys
# from wit import Wit
from datetime import datetime, timezone

import dialogflow_v2 as dialogflow

from aiohttp_json_rpc import JsonRpcClient


access_token = "MJGNIFPBRIAL2UPSTYDV4Z4P5A6Z5D4G"

DIALOGFLOW_PROJECT_ID = 'reminders-xudwgy'
DIALOGFLOW_LANGUAGE_CODE = 'en-US'
GOOGLE_APPLICATION_CREDENTIALS = '1234567abcdef.json'
SESSION_ID = 'current-user-id'

class Sentiment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session_client = dialogflow.SessionsClient()
    
    # async def rpc_call(self, method, args):
    #     rpc_client = JsonRpcClient()
    #     try:
    #         print("-"*20)
    #         print("connecting to RPC")
    #         await rpc_client.connect("127.0.0.1", 6133)
    #         call_result = await rpc_client.call(method, args)
    #         print("-"*20)
    #         print(call_result)
    #         print("-"*20)
    #
    #     except Exception as e:
    #         print("-"*20)
    #         print(e)
    #         print("-"*20)
    #
    #     finally:
    #         print("-"*20)
    #
    #         await rpc_client.disconnect()
    #         return call_result
    #
    #
    # @commands.command()
    # async def enable(self, ctx, message):
    #     # response = self.client.message(msg=message, context={'session_id':ctx.channel.id})
    #     # await self.handle_message(response=response)
    #     await ctx.send('ModMail enabled')
    #
    # @commands.Cog.listener()
    # async def on_message(self, message: discord.Message):
    #     # if message.author.id != 280730525960896513:
    #     #     return
    #     if message.author.bot: return
    #     # if message.channel.id != 590945364551401482 or 133251234164375552:
    #     #     return
    #     allowed = [57287406247743488, 280730525960896513]
    #     if message.author.id not in allowed : return
    #     ctx = await self.bot.get_context(message)
    #     prefixes = await self.bot.db.prefix()
    #     if message.content.startswith(tuple(prefixes)):
    #         return
    #     response = self.client.message(msg=message.content, context={'session_id':message.channel.id})
    #     await self.handle_message(response=response, ctx=ctx)
    #
    # async def first_entity_value(self, entities, entity):
    #     """
    #     Returns first entity value
    #     """
    #     if entity not in entities:
    #         return None
    #     val = entities[entity][0]['value']
    #     con = entities[entity][0]['confidence']
    #     if not val:
    #         return None
    #     return {
    #         "val": val['value'] if isinstance(val, dict) else val,
    #         "confidence": con
    #     }
    #
    # async def second_entity_value(self, entities, entity):
    #     """
    #     Returns second entity value
    #     """
    #     if entity not in entities:
    #         return None
    #     val = entities[entity][0]['value']
    #     con = entities[entity][1]['confidence']
    #     if not val:
    #         return None
    #     return {
    #         "val": val['value'] if isinstance(val, dict) else val,
    #         "confidence": con
    #     }
    #
    # async def handle_message(self, response, ctx):
    #     """
    #     Customizes our response to the message and sends it
    #     """
    #     channel = ctx.channel
    #     prefix_list = await self.bot.db.prefix()
    #     prefix_string = ", ".join(prefix_list)
    #     entities = response['entities']
    #     print("-" * 10)
    #
    #     greetings = await self.first_entity_value(entities, 'greetings')
    #     print(f"greeting: {greetings}")
    #
    #     dates = await self.first_entity_value(entities, 'datetime')
    #     print(f"date {dates}")
    #
    #     distance = await self.first_entity_value(entities, 'distance')
    #     print(f"Distance: {distance}")
    #
    #     modmail = await self.first_entity_value(entities, 'modmail')
    #     print(f"Modmail: {modmail}")
    #
    #     red_prefix = await self.first_entity_value(entities, 'red_prefix')
    #     print(f"red_prefix: {red_prefix}")
    #
    #     red_help = await self.first_entity_value(entities, 'red_help')
    #     print(f"red_help: {red_help}")
    #
    #     print("-" * 10)
    #
    #     if greetings:
    #         text = f"({greetings['confidence']*100:.0f}%) - Howdy! :cowboy:"
    #     elif red_help:
    #         text = f"({red_help['confidence']*100:.0f}%) - :cowboy: Wow. Calm down there, have you tried `[p]help`?  "
    #     elif red_prefix:
    #         text = f"({red_prefix['confidence']*100:.0f}%) - If you're looking for my prefix, you can use one of these: `{prefix_string}` "
    #
    #     elif modmail:
    #         toggle = await self.first_entity_value(entities, 'on_off')
    #         if toggle['val'] == 'on':
    #             text = f"You want to turn modmail `ON`, I'm ` {toggle['confidence']*100:.0f}% ` certain."
    #             # cog = self.bot.get_cog('Core')
    #             cmd = self.bot.get_command('load')
    #             await ctx.invoke(cmd, 'modmail')
    #         else:
    #             text = f"You want to turn modmail `OFF`, I'm ` {toggle['confidence']*100:.0f}% ` certain."
    #             cmd = self.bot.get_command('unload')
    #             await ctx.invoke(cmd, 'modmail')
    #     elif dates:
    #         dt_aware = datetime.fromisoformat(dates['val'])
    #         date_time = dt_aware.strftime("%m/%d/%Y, %H:%M")
    #
    #         now = datetime.now(timezone.utc)
    #
    #         delta = (dt_aware - now)
    #         print(delta)
    #         text = f"({dates['confidence']*100:.0f}%) -  I understood your message as a DateTime\n\nDateTime: ` {date_time} `\n\nDelta: `{delta}` "
    #     elif distance:
    #         text = f"({distance['confidence']*100:.0f}%) - I understood your message as containing a distance"
    #     else:
    #         print("I've received your message: " + response['_text'])
    #     # send message
    #     dest = self.bot.get_channel(channel)
    #     try:
    #         await channel.send(text)
    #     except UnboundLocalError:
    #         pass


