import os
import json

from redbot.core.data_manager import cog_data_path

from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions


async def yes_or_no(ctx, user):
    msg = await ctx.send(f"Send message to {user.name}?")
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
