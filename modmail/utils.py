import discord
from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions
import logging

log = logging.getLogger("red.breadcogs.modmail")

ERROR = "⛔"
WARNING = "💬"


async def yes_or_no(ctx, message):
    msg = await ctx.send(message)
    start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)

    pred = ReactionPredicate.yes_or_no(msg, ctx.author)
    await ctx.bot.wait_for("reaction_add", check=pred)
    await msg.delete()
    return pred.result


async def alert_message_embed(message: discord.Message):
    author = message.author

    attachments_urls = [
        message.attachments.url for message.attachments in message.attachments
    ]
    attached_list = "\n".join(attachments_urls)

    if message.attachments:
        attachments_string = f"**Attachments**\n {attached_list}"
    else:
        attachments_string = f" "

    description = (
        f"**Author** \n"
        f" `{author.name}#{author.discriminator}` \n"
        f" `{author.id}` \n\n"
        f"**Message Content**\n"
        f"```{message.content}```\n"
        f"{attachments_string}"
    )
    embed = discord.Embed(
        title="📬 New ModMail recieved",
        description=description,
        color=discord.Color.green(),
    )
    embed.set_thumbnail(url=f"{author.avatar_url}")
    embed.set_footer(text=f"MSG ID: {message.id}")
    return embed


async def author_to_json(author):
    json_author = {
        "id": author.id,
        "name": author.name,
        "discriminator": author.discriminator,
        "avatar": str(author.avatar_url),
        "created_at": author.created_at.isoformat(),
    }
    return json_author


async def modmail_message_to_json(message: discord.Message, alert) -> dict:
    author = message.author
    json_author = await author_to_json(author)

    # attachments = [
    #         message.attachments.url for message.attachments in message.attachments
    #     ]

    json_message = {
        "id": message.id,
        "author": json_author,
        "attachments": message.attachments,
        "content": message.content,
    }

    final_json = {
        "id": message.id,
        "alert_message": {"channel": alert.channel_id, "message": alert.message_id},
        "status": "new",
        "assigned": False,
        "mod_assigned": None,
        "created_at": message.created_at.strftime("%m/%d/%Y, %H:%M"),
        "thread": json_message,
        "reply": {},
    }
    return final_json


async def modmail_reply_to_json(ctx_message: discord.Message, reply_content) -> dict:
    author = ctx_message.author

    json_author = await author_to_json(author)
    json_message = {
        "id": ctx_message.id,
        "author": json_author,
        "content": reply_content,
    }

    final_json = {
        "id": ctx_message.id,
        "created_at": ctx_message.created_at.strftime("%m/%d/%Y, %H:%M"),
        "thread": json_message,
    }
    return final_json


async def multi_guild_finder(all_members, author: discord.User):
    shared_guilds = [member.guild for member in all_members if member.id == author.id]
    return shared_guilds


# message handlers
async def send_error_message(destination, message):
    await destination.send(f"{ERROR} {message}")


async def send_warning_message(destination, message):
    await destination.send(f"{WARNING} {message}")