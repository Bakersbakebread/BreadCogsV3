from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.predicates import ReactionPredicate


async def yes_or_no(ctx, message,) -> bool:
    msg = await ctx.send(message)
    start_adding_reactions(
        msg, ReactionPredicate.YES_OR_NO_EMOJIS,
    )

    pred = ReactionPredicate.yes_or_no(msg, ctx.author,)
    await ctx.bot.wait_for(
        "reaction_add", check=pred,
    )
    await msg.delete()
    return pred.result
