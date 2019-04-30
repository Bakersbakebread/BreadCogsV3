from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions

async def yes_or_no ( ctx, user ):
    msg = await ctx.send(f"Send message to {user.name}?")
    start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)

    pred = ReactionPredicate.yes_or_no(msg, ctx.author)
    await ctx.bot.wait_for("reaction_add", check = pred)
    await msg.delete()
    return pred.result