import discord
import asyncio
from redbot.core import Config

from redbot.core.utils.chat_formatting import humanize_list

CATEGORY_NAME = "📬 ModMail"
CONFIG = Config.get_conf(
    None, identifier=2807305259608965131, cog_name="ModMail")
NEW_THREAD_ICON = "📬"


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


class MailCategory:
    def __init__(self, bot, ctx):
        self.bot = bot
        self.ctx = ctx
        self.guild = ctx.guild
        self.config = Config.get_conf(None, identifier=2807305259608965131, cog_name="ModMail")

        self.category_name = "📬 ModMail"

        self.manage_messages_roles = self.get_allowed_roles()
        self.overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }

    async def make_new_modmail(self):
        for role in self.manage_messages_roles:
            self.overwrites[role] = discord.PermissionOverwrite(read_messages=True)
        # create the category
        try:
            category = await self.ctx.guild.create_category(
                name=CATEGORY_NAME, overwrites=self.overwrites
            )
            await self.config.guild(self.ctx.guild).category_id.set(category.id)
        except discord.errors.Forbidden:
            return await self.ctx.send("Missing permissions to create category")

        # create the help & log channel
        try:
            help_channel = await self.ctx.guild.create_text_channel(
                name="Help", category=category
            )

            log_channel = await self.ctx.guild.create_text_channel(
                name="ModMail Log", category=category
            )
        except discord.errors.Forbidden:
            return await self.ctx.send("Missing permissions to create channels")

        help_embeds = await self.display_help_embed()
        for embed in help_embeds:
            await help_channel.send(embed=embed)

        await self.config.guild(self.guild).help_message_id.set(help_channel.id)
        await self.config.guild(self.guild).log_channel_id.set(log_channel.id)

    async def display_help_embed(self) -> list:
        embeds = []

        setup = discord.Embed(
            title="ModMail Help", description=("""Description to go here I guess""")
        )
        help_channel = await self.config.guild(self.guild).help_message_id()
        log_channel_id = await self.config.guild(self.guild).log_channel_id()

        setup.add_field(name="Help Channel", value=help_channel)
        setup.add_field(name="Log Channel", value=log_channel_id)

        settings_active = discord.Embed(title="⚙️ Active ModMail Settings")

        settings_active.add_field(
            name="✔️ Active Settings", value="Setting 1\nSetting 2\nSetting 3"
        )

        settings_active.add_field(
            name="❌ Disabled Settings", value="Setting 1\nSetting 2\nSetting 3"
        )

        embeds.append(setup)
        embeds.append(settings_active)

        return embeds

    def get_allowed_roles(self) -> list:
        """Function to search through roles and append to list of matching permission"""
        roles = []
        # await ctx.send("Scanning all roles:")
        for r in self.guild.roles:
            # await ctx.send(f"Role: {r}")
            if r.permissions.manage_messages:
                roles.append(r)
            # await ctx.send(f"```Permissions Valid: {r}```")
        return roles


class MailThread:
    def __init__(self, bot, user, guild):
        self.user = user
        self.guild = guild

        self.thread_name = f"{NEW_THREAD_ICON}-{self.user.name}-{self.user.id}"

    async def send_to_channel(self, channel):
        print(self.user, self.guild)
        print(channel)

    async def make_new_channel(self) -> None:
        category = discord.utils.get(self.guild.categories, name=CATEGORY_NAME)
        try:
            new_thread = await self.guild.create_text_channel(
                name=self.thread_name,
                category=category,
                topic=await format_channel_topic(self.user),
                reason=f"New ModMail Thread for {self.user.name}",
            )
        except discord.errors.Forbidden as e:
            print(f"[ModMail] {e} - could not create channel.")
            return False

        if not category:
            # TODO: Move into DM owner?
            category_error = "Could not assign channel to ModMail Category."
            owner = await self.bot.get_user_info(self.bot.owner_id)

            await owner.send(category_error)
            await new_thread.send(category_error)

        await new_thread.send(embed=await user_info_embed(self.user))
