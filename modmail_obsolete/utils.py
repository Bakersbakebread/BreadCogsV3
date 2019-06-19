import os
import json

from redbot.core.data_manager import cog_data_path

from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions


async def yes_or_no(ctx, message):
    msg = await ctx.send(message)
    start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)

    pred = ReactionPredicate.yes_or_no(msg, ctx.author)
    await ctx.bot.wait_for("reaction_add", check=pred)
    await msg.delete()
    return pred.result


async def get_label(severity, label):
    with open(
        os.path.join(cog_data_path(raw_name="ModMail"), "dictionary.json")
    ) as json_file:
        data = json.load(json_file)
    return data[severity][label]


async def save_message_to_config(config, author, embed):
    async with config.user(author).info() as user_info:
        user_info["current_thread"].append(embed.to_dict())
