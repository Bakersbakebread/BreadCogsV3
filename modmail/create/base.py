import discord
from redbot.core import Config

CATEGORY_NAME = "📬 ModMail"
CONFIG = Config.get_conf(None, identifier=2807305259608965131, cog_name="ModMail")

async def get_allowed_roles(ctx) -> list:
	"""Function to search through roles and append to list of matching permission"""
	roles = []
	# await ctx.send("Scanning all roles:")
	for r in ctx.guild.roles:
		# await ctx.send(f"Role: {r}")
		if r.permissions.manage_messages:
			roles.append(r)
			# await ctx.send(f"```Permissions Valid: {r}```")
	return roles

	
async def display_help_embed(guild) -> list:
	embeds = []

	setup = discord.Embed(
		title="ModMail Help", description=("""Description to go here I guess""")
	)
	help_channel = await CONFIG.guild(guild).help_message_id()
	log_channel_id = await CONFIG.guild(guild).log_channel_id()

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
		category = await ctx.guild.create_category(
			name=CATEGORY_NAME, overwrites=overwrite
		)
		await config.guild(ctx.guild).category_id.set(category.id)
	except discord.errors.Forbidden:
		return await ctx.send("Missing permissions to create category")

	# create the help & log channel
	try:
		help_channel = await ctx.guild.create_text_channel(
			name="Help", category=category
		)

		log_channel = await ctx.guild.create_text_channel(
			name="ModMail Log", category=category
		)

	except discord.errors.Forbidden:
		return await ctx.send("Missing permissions to create channels")

	help_embeds = await display_help_embed(ctx.guild)

	for embed in help_embeds:
		await help_channel.send(embed=embed)

	await config.guild(ctx.guild).help_message_id.set(help_channel.id)
	await config.guild(ctx.guild).log_channel_id.set(log_channel.id)