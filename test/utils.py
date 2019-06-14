import discord

async def modmail_message_to_json(message: discord.Message) -> dict:
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
        "created_at": message.created_at.isoformat(),
        "type": str(message.type),
    }
    final_json = {
        "id": message.id,
        "status":"new",
        "thread":json_message
    }
    return final_json

async def multi_guild_finder(all_members, author:discord.User):
    shared_guilds = [member.guild for member in all_members if member.id == author.id]
    return shared_guilds