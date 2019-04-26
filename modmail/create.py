import discord
import asyncio

CATEGORY_NAME = "📬 ModMail"
NEW_THREAD_ICON = "🔴"


async def get_allowed_roles(ctx):
    """Function to search through roles and append to list of matching permission"""
    roles = []
    # await ctx.send("Scanning all roles:")
    for r in ctx.guild.roles:
        # await ctx.send(f"Role: {r}")
        if r.permissions.manage_messages:
            roles.append(r)
            # await ctx.send(f"```Permissions Valid: {r}```")
    return roles

async def user_info_embed(user):
    embed = discord.Embed(title=f"👤 {user.name} - {user.id}",
        description="""Information about user:""" ,)
    embed.set_thumbnail(url=user.avatar_url)
    
    return embed

async def display_help_embed():
    embeds = []
    
    setup = discord.Embed(title='ModMail Help',
        description=("""Description to go here I guess"""))
    setup.add_field(name="👍", value="Help Channel")
    setup.add_field(name="👍", value="ModMail Log Channel")
    setup.add_field(name="👎", value="Another SEttings")

    settings_active = discord.Embed(title="⚙️ Active ModMail Settings",)

    settings_active.add_field(name="✔️ Active Settings", 
        value="Setting 1\nSetting 2\nSetting 3")

    settings_active.add_field(name="❌ Disabled Settings", 
        value="Setting 1\nSetting 2\nSetting 3")

    embeds.append(setup)
    embeds.append(settings_active)

    return embeds

async def format_channel_topic(user):
    topic = f"**User** : {user.name}#{user.discriminator}\n"
    topic += f"**ID** : {user.id}\n\n"

    # created_at = user.created_at.strftime("%b %d %Y")
    # joined_at = user.joined_at.strftime("%b %d %Y")

    # topic += f"**Created** : {created_at}\n"
    # topic += f"**Joined** : {joined_at}\n"

    return topic

async def new_modmail(ctx, config):
    """Set up the categories and channels for modmail."""
    # function to help find who can manage messages
    manage_messages_roles = await get_allowed_roles(ctx)
    # @everyone won't be able to see, but everyone with manage guild can
    # this will umbrella the cat to every channel
    overwrite = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False)
    }
    for role in manage_messages_roles:
        overwrite[role] = discord.PermissionOverwrite(read_messages=True)
    # create the category
    try:
        category = await ctx.guild.create_category(name=CATEGORY_NAME, overwrites=overwrite)
    except discord.errors.Forbidden:
        return await ctx.send("Missing permissions to create category")

    # create the help & log channel
    try:
        help_channel = await ctx.guild.create_text_channel(name='Help',
            category=category)

        log_channel = await ctx.guild.create_text_channel(name='ModMail Log',
            category=category)

    except discord.errors.Forbidden:
        return await ctx.send("Missing permissions to create channels")
    
    help_embeds = await display_help_embed()

    for embed in help_embeds:
        await help_channel.send(embed=embed)
        
    await config.guild(ctx.guild).help_message_id.set(help_channel.id)
    await ctx.send(f'Help channel ID stored: {help_channel.id}')
    await config.guild(ctx.guild).log_channel_id.set(log_channel.id)
    await ctx.send(f'Log ID stored: {log_channel.id}')

async def new_modmail_thread(bot, guild, user):
    thread_name = f"{NEW_THREAD_ICON}-{user.name}-{user.id}"

    category = discord.utils.get(guild.categories, name=CATEGORY_NAME)


    try:
        new_thread = await guild.create_text_channel(
            name=thread_name,
            category=category,
            topic=await format_channel_topic(user),
            reason=f"New ModMail Thread for {user.name}")
    except discord.errors.Forbidden as e:
        print(f"[ModMail] {e} - could not create channel.")
        return False
        
    if not category:
        # TODO: Move into DM owner?
        category_error = "Could not assign channel to ModMail Category."
        owner = await bot.get_user_info(bot.owner_id)
        await owner.send(category_error)
        await new_thread.send(category_error)
    
    await new_thread.send(embed = await user_info_embed(user))

    return new_thread
