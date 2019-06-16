import discord
from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions

async def yes_or_no(ctx, message):
    msg = await ctx.send(message)
    start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)

    pred = ReactionPredicate.yes_or_no(msg, ctx.author)
    await ctx.bot.wait_for("reaction_add", check=pred)
    await msg.delete()
    return pred.result

async def modmail_message_to_json(message: discord.Message, alert) -> dict:
    author = message.author
    json_author = {
        "id": author.id,
        "name": author.name,
        "discriminator": author.discriminator,
        "avatar": str(author.avatar_url),
        "created_at": author.created_at.isoformat(),
    }
    json_message = {
        "id": message.id,
        "author": json_author,
        "attachments": [
            message.attachments.url for message.attachments in message.attachments
        ],
        "content": message.content,
    }
    final_json = {
        "id": message.id,
        "alert_message_id": alert.id,
        "status":"new",
        "assigned":False,
        "mod_assigned":None,
        "created_at": message.created_at.isoformat(),
        "thread":json_message
    }
    return final_json

async def multi_guild_finder(all_members, author:discord.User):
    shared_guilds = [member.guild for member in all_members if member.id == author.id]
    return shared_guilds