import discord
import asyncio
from redbot.core import Config

from redbot.core.utils.chat_formatting import humanize_list


CONFIG = Config.get_conf(None, identifier=2807305259608965131, cog_name="ModMail")


async def user_info_embed(user):
    embed = discord.Embed(
        title=f"{user.name} - {user.id}", description="""Information about user:"""
    )
    embed.set_thumbnail(url=user.avatar_url)

    created_at = user.created_at.strftime("%b %d %Y")
    # joined_at = user.joined_at.strftime("%b %d %Y")
    async with CONFIG.user(user).info() as user_info:
        history = len(user_info["archive"])
    embed.add_field(name="Joined Discord", value=created_at)
    embed.add_field(name="Amount of previous threads", value=history)
    # embed.add_field(name="User's Roles",
    #                value = humanize_list([x.name for x in user.roles]),
    #                inline=False)

    return embed

async def format_channel_topic(user):
    topic = f"**User** : {user.name}#{user.discriminator}\n"
    topic += f"**ID** : {user.id}\n\n"
    return topic

async def new_modmail_thread(bot, guild, user):
    thread_name: str = f"{NEW_THREAD_ICON}-{user.name}-{user.id}"

    category = discord.utils.get(guild.categories, name=CATEGORY_NAME)

    try:
        new_thread = await guild.create_text_channel(
            name=thread_name,
            category=category,
            topic=await format_channel_topic(user),
            reason=f"New ModMail Thread for {user.name}",
        )
    except discord.errors.Forbidden as e:
        print(f"[ModMail] {e} - could not create channel.")
        return False

    if not category:
        # TODO: Move into DM owner?
        category_error = "Could not assign channel to ModMail Category."
        owner = await bot.get_user_info(bot.owner_id)
        await owner.send(category_error)
        await new_thread.send(category_error)

    await new_thread.send(embed=await user_info_embed(user))

    return new_thread